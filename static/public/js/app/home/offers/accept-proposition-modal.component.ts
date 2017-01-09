import {
    Component, ViewEncapsulation, OnInit, style,
    animate, transition, state, trigger, Output, EventEmitter
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
import {OfferGet, Account} from "../profile/account";

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
    user: Account = new Account;
    pendingOffers: Array<OfferGet> = [];
    currentOfferGet: OfferGet = new OfferGet;
    proposer: User = new User;
    itemProposed: DetailedItem = new DetailedItem;
    itemWanted: DetailedItem = new DetailedItem;
    starsCount: number;
    displayRating: boolean = true;

    @Output() seeProfileEvent = new EventEmitter();

    constructor (private authService: AuthService,
                 private itemsService: ItemsService,
                 private offerService: OfferService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        // Listen for user login
        this.subscription = this.authService.accountSelected$.subscribe(
            user => {
                this.user = user;
                console.log(user);

                // Get the offers and add them to pending offers array
                for (let pendingOffer of this.user.pending_offers) {
                    this.pendingOffers.push(pendingOffer);
                }

                // Get the current pending offer
                this.currentOfferGet = this.nextOffer();

                // Get data related to it
                if (this.currentOfferGet !== null) {
                    this.getUserOffer(this.currentOfferGet.item_received);
                    this.getProposerOffer(this.currentOfferGet.item_given);
                }
            }
        );

    }

    acceptOffer() {
        console.log("offer accepted");
        this.displayRating = true;
    }

    validOffer() {
        // Send the accepted offer with message
        let offerUpdate = new OfferUpdate(true, true);

        this.offerService.updateOffer(this.currentOfferGet.id, offerUpdate).then(
            res => {
                // Rate the proposer
                this.displayRating = true;
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

    rateProposer() {
        console.log(this.starsCount);
        let note = new Note(this.currentOfferGet.id, this.starsCount);

        this.offerService.rateUser(note).then(
            res => {
                this.toastr.success("Thank you for rating", "Offer accepted !");

                // Get next offer
                this.nextOffer();
            },
            error => this.toastr.error("You accepted this offer!", "Error")
        );
    }

    seeProfile() {
        this.seeProfileEvent.emit(this.proposer);
    }

    sendMessage() {
        this.toastr.warning("to " + this.proposer.first_name + " " + this.proposer.last_name, "Send message");
    }
}
