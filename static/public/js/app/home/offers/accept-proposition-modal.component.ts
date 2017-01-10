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
    currentOfferGet: OfferGet = new OfferGet;
    proposer: User = new User;
    itemProposed: DetailedItem = new DetailedItem;
    itemWanted: DetailedItem = new DetailedItem;
    starsCount: number;
    displayRating: boolean = false;
    offerUpdate: OfferUpdate;

    @Output() seeProfileEvent = new EventEmitter();
    @Output() removeOnePendingOfferEvent = new EventEmitter();

    constructor (private authService: AuthService,
                 private itemsService: ItemsService,
                 private offerService: OfferService,
                 private profileService: ProfileService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        // Listen for user login
        this.subscription = this.authService.accountSelected$.subscribe(
            user => {
                this.nextOffer();
            }
        );
    }

    acceptOffer() {
        this.displayRating = true;
        this.offerUpdate = new OfferUpdate(true, "I accept your offer. Contact me at " + this.user.email);

        // Accept offer then rate user
        this.offerService.updateOffer(this.currentOfferGet.id, this.offerUpdate).then(
            res => {
                this.starsCount = 0;
                this.displayRating = true;
            },
            error => {
                this.displayRating = false;
                this.toastr.error(error, "Error");
            }
        );
    }

    refuseOffer() {
        this.offerUpdate = new OfferUpdate(false, "Thank's for your proposition but I refuse your offer.");

        this.offerService.updateOffer(this.currentOfferGet.id, this.offerUpdate).then(
            res => {
                this.toastr.success("", "Offer Refused");
                this.removeOnePendingOfferEvent.emit();
                this.displayRating = false;
                // Get next offer
                this.nextOffer();
            },
            error => this.toastr.error(error, "Error")
        );
    }

    // We must get the pending offers again because they might be updated by previous actions
    nextOffer() {
        this.authService.getAccount().then(
            account => {
                this.user = account;
                if (this.user.pending_offers.length > 0) {
                    this.currentOfferGet = this.user.pending_offers.pop();
                    this.getUserOffer(this.currentOfferGet.item_received);
                    this.getProposerOffer(this.currentOfferGet.item_given);
                } else {
                    this.currentOfferGet = null;
                    this.displayRating = false;
                }
            },
            error => this.toastr.error(error, "Error")
        );
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
        this.offerService.rateUser(note).then(
            res => {
                this.toastr.success("Thank you for rating", "Offer accepted !");

                this.displayRating = false;
                this.starsCount = 0;

                this.removeOnePendingOfferEvent.emit();
                // Get next offer
                this.nextOffer();
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

    showItem(item: DetailedItem): void {
        this.itemsService.selectItem(item);
    }
}
