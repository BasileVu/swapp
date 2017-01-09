import {
    Component, ViewEncapsulation, OnInit, style,
    animate, transition, state, trigger, Output, EventEmitter, OnChanges, Input,
    SimpleChanges
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
import {ProfileService} from "../profile/profile.service";

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
export class AcceptPropositionModalComponent implements OnInit, OnChanges {

    subscription: Subscription;
    user: Account = new Account;
    pendingOffers: Array<OfferGet> = [];
    @Input() currentOfferGet: OfferGet = new OfferGet;
    proposer: User = new User;
    itemProposed: DetailedItem = new DetailedItem;
    itemWanted: DetailedItem = new DetailedItem;
    starsCount: number;
    displayRating: boolean = false;
    offerUpdate: OfferUpdate;

    @Output() seeProfileEvent = new EventEmitter();
    @Output() setNumberOfPendingOfferEvent = new EventEmitter();

    constructor (private authService: AuthService,
                 private itemsService: ItemsService,
                 private offerService: OfferService,
                 private profileService: ProfileService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        // Listen for user login
        this.subscription = this.authService.accountSelected$.subscribe(
            user => {
                this.user = user;
                console.log("user");
                console.log(this.user);

                // Get the offers and add them to pending offers array
                for (let pendingOffer of this.user.pending_offers) {
                    for (let item of this.user.items) {
                        if (item === pendingOffer.item_received) {
                            this.pendingOffers.push(pendingOffer);
                            break;
                        }
                    }
                }

                // Get the current pending offer
                this.nextOffer();
            }
        );
    }

    ngOnChanges(changes: SimpleChanges) {
    }

    acceptOffer() {
        this.displayRating = true;
        this.offerUpdate = new OfferUpdate(true, "I accept your offer. Contact me at " + this.user.email);
    }

    refuseOffer() {
        this.offerUpdate = new OfferUpdate(false, "Thank's for your proposition but I refuse your offer.");

        this.offerService.updateOffer(this.currentOfferGet.id, this.offerUpdate).then(
            res => {
                this.toastr.success("", "Offer Refused");
                this.setNumberOfPendingOfferEvent.emit(1);
                // Get next offer
                this.nextOffer();
            },
            error => this.toastr.error(error, "Error")
        );
    }

    nextOffer() {
        if (this.pendingOffers.length > 0) {
            this.currentOfferGet = this.pendingOffers.pop();
            this.getUserOffer(this.currentOfferGet.item_received);
            this.getProposerOffer(this.currentOfferGet.item_given);
        } else {
            this.currentOfferGet = null; // no next offers
            this.displayRating = false;
        }
        console.log(this.currentOfferGet);
    }

    getUserOffer(item_wanted: number) {
        this.itemsService.getDetailedItem(item_wanted).then(
            itemWanted => {
                this.itemWanted = itemWanted;
            },
            error => this.toastr.error(error, "Error")
        );
    }

    getProposerOffer(item_proposed: number) {
        this.itemsService.getDetailedItem(item_proposed).then(
            itemProposed => {
                this.itemProposed = itemProposed;

                // Get proposer data
                this.itemsService.getUser(this.itemProposed.owner_username).then(
                    proposer => {
                        this.proposer = proposer;
                    },
                    error => this.toastr.error(error, "Error")
                )
            },
            error => this.toastr.error(error, "Error")
        );
    }

    rateProposer() {
        let note = new Note(this.currentOfferGet.id, "Default message", this.starsCount);

        // Accept offer then rate user
        this.offerService.updateOffer(this.currentOfferGet.id, this.offerUpdate).then(
            res => {
                this.offerService.rateUser(note).then(
                    res => {
                        this.toastr.success("Thank you for rating", "Offer accepted !");

                        this.displayRating = false;
                        this.starsCount = 0;

                        this.setNumberOfPendingOfferEvent.emit(1);
                        // Get next offer
                        this.nextOffer();
                    },
                    error => this.toastr.error(error, "Error")
                );
            },
            error => this.toastr.error(error, "Error")
        );

    }

    seeProfile() {
        this.seeProfileEvent.emit(this.proposer);
    }

    sendMessage() {
        this.toastr.warning("to " + this.proposer.first_name + " " + this.proposer.last_name, "Send message");
    }
}
