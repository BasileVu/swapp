import {
    Component, ViewEncapsulation, OnInit, style,
    animate, transition, state, trigger
} from '@angular/core';
import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";
import {User} from "../profile/user";
import {DetailedItem} from "../items/detailed-item";
import {ItemsService} from "../items/items.service";
import {OfferUpdate} from "./offer-update";
import {OfferService} from "./offers.service";
import {ToastsManager} from "ng2-toastr/ng2-toastr";
import {Note} from "./Note";

export class PendingOffer {
    id: number;
    accepted: boolean;
    answered: boolean;
    comment: string;
    item_given: number;
    item_received: number;

    constructor() {
        this.id = 0;
        this.accepted = false;
        this.answered = false;
        this.comment = "";
        this.item_given = 0;
        this.item_received = 0;
    }
}

@Component({
    moduleId: module.id,
    selector: 'accept-proposition-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './accept-proposition-modal.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({transform: 'translateX(0) scale(1.1)'})),
            transition('void => *', [
                style({transform: 'translateX(0) scale(0)'}),
                animate('0.2s ease-in')
            ]),
            transition('* => void', [
                animate('0.2s 10 ease-out', style({transform: 'translateX(0) scale(0)'}))
            ])
        ])
    ]
})
export class AcceptPropositionModalComponent implements OnInit {

    subscription: Subscription;
    user: User = new User;
    pendingOffers: Array<PendingOffer> = [];
    currentPendingOffer: PendingOffer = new PendingOffer;
    proposer: User = new User;
    itemProposed: DetailedItem = new DetailedItem;
    itemWanted: DetailedItem = new DetailedItem;
    displayMessage: boolean;
    displayRating: boolean;

    constructor (private authService: AuthService,
                 private itemsService: ItemsService,
                 private offerService: OfferService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        // Listen for user login
        this.subscription = this.authService.userSelected$.subscribe(
            user => {
                this.user = user;

                // Get the offers and add them to pending offers array
                for (let pendingOffer of this.user.pending_offers) {
                    this.pendingOffers.push(pendingOffer);
                }

                // Get the current pending offer
                this.currentPendingOffer = this.nextOffer();

                // Get data related to it
                this.getUserOffer(this.currentPendingOffer.item_received);
                this.getProposerOffer(this.currentPendingOffer.item_given);
            }
        );

    }

    acceptOffer() {
        console.log("offer accepted");
        this.displayMessage = true;

        // Get next offer
        this.nextOffer();
    }

    validOffer() {
        // Send the accepted offer with message
        let offerUpdate = new OfferUpdate(true, true);

        this.offerService.updateOffer(this.currentPendingOffer.id, offerUpdate).then(
            res => {
                // Rate the proposer
                this.displayRating = true;

                // TODO : Rate the proposer
                this.rateProposer(5);
            },
            error => this.toastr.error(error, "Error")
        )
    }

    refuseOffer() {
        console.log("offer refused");
        // Inform the proposer

        // Get next offer
        this.nextOffer();
    }

    nextOffer() {
        if (this.pendingOffers.length > 0)
            return this.pendingOffers.pop();
        else
            return null;
    }

    getUserOffer(item_wanted: number) {
        this.itemsService.getDetailedItem(item_wanted).then(
            item => {
                this.itemWanted = item;
            }
        );
    }

    getProposerOffer(item_proposed: number) {
        this.itemsService.getDetailedItem(item_proposed).then(
            item => {
                this.itemProposed = item;

                // Get proposer data
                this.itemsService.getUser(this.itemProposed.owner_username).then(
                    proposer => {
                        this.proposer = proposer;
                    }
                )
            }
        );
    }

    rateProposer(star: number) {
        let note = new Note(this.currentPendingOffer.id, star);

        this.offerService.rateUser(note).then(
            res => {
                this.toastr.success("Thank you for rating", "Offer accepted !");
            },
            error => this.toastr.error("You accepted this offer!", "Error")
        );
    }
}
