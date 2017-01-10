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
import { __platform_browser_private__,
    DomSanitizer } from '@angular/platform-browser';


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
    ],
    providers: [__platform_browser_private__.BROWSER_SANITIZATION_PROVIDERS]
})
export class AcceptPropositionModalComponent implements OnInit {

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
    @Output() showItemFromAcceptOfferEvent = new EventEmitter();

    constructor (private authService: AuthService,
                 private itemsService: ItemsService,
                 private offerService: OfferService,
                 private profileService: ProfileService,
                 public toastr: ToastsManager,
                 private sanitizer: DomSanitizer) {}

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
                this.removeOnePendingOfferEvent.emit(null);
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
                this.sanitizer.bypassSecurityTrustUrl(this.user.profile_picture_url);

                let leave = false;
                this.currentOfferGet = null;
                // Get the offers and add them to pending offers array
                for (let pendingOffer of this.user.pending_offers) {
                    for (let item of this.user.items) {
                        if (item === pendingOffer.item_received) {
                            this.currentOfferGet = pendingOffer;
                            leave = true;
                            break;
                        }
                    }
                    if (leave) break;
                }

                if (this.currentOfferGet !== null) {
                    this.getUserOffer(this.currentOfferGet.item_received);
                    this.getProposerOffer(this.currentOfferGet.item_given);
                } else {
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
                this.sanitizer.bypassSecurityTrustUrl(this.itemWanted.images[0].url);
            },
            error => this.toastr.error(error, "Error")
        );
    }

    getProposerOffer(item_proposed: number) {
        this.itemsService.getDetailedItem(item_proposed).then(
            itemProposed => {
                this.itemProposed = itemProposed;
                this.sanitizer.bypassSecurityTrustUrl(this.itemProposed.images[0].url);

                // Get proposer data
                this.itemsService.getUser(this.itemProposed.owner_username).then(
                    proposer => {
                        this.proposer = proposer;
                        this.sanitizer.bypassSecurityTrustUrl(this.proposer.profile_picture_url);
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

                this.removeOnePendingOfferEvent.emit(null);
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
        this.showItemFromAcceptOfferEvent.emit(item);
    }
}
