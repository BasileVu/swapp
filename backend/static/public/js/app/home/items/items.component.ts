import {Component, ViewEncapsulation, OnInit} from '@angular/core';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { ItemsService } from './items.service';

import { DetailedItem } from './detailed-item';
import {Subscription} from "rxjs";
import {AuthService} from "../../shared/authentication/authentication.service";
import {OfferService} from "../offers/offers.service";
import {User} from "../profile/user";

declare let $: any;

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html'
})
export class ItemsComponent implements OnInit {

    items: Array<DetailedItem>;
    loggedIn: boolean;
    user: User;
    subscription: Subscription;
    infoMessage: string = "Loading items...";

    constructor (private itemsService: ItemsService,
                 private authService: AuthService,
                 private offerService: OfferService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        this.items = [];
        this.getItems();

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                this.loggedIn = loggedIn;
                this.getItems();
            }
        );

        // Listen for user login
        this.subscription = this.authService.userSelected$.subscribe(
            user => {
                this.user = user;
            }
        );

        this.itemsService.getItemsSubject().subscribe((items: DetailedItem[]) => {
            this.items = items;
            if (items.length === 0)
                this.infoMessage = "No item found";
            else
                this.infoMessage = "Loading items...";
        });
    }

    getItems() {
        this.itemsService.getItems()
            .then(
                items => {
                    this.items = [];
                    this.items = items
                },
                error => this.toastr.error(error, "Error")
            );
    }

    gotoDetail(item: DetailedItem): void {
        // Inform the item modal about the item we just clicked.
        // (ItemComponent and ItemModalComponent communicate via ItemService)
        this.itemsService.selectItem(item);
    }

    searchCategory(category_id: number) {
        this.toastr.warning("for this '" + category_id + "' (TODO)", "Search category");
        // TODO
    }

    searchLocation(location: string) {
        this.toastr.warning("for this '" + location + "' (TODO)", "Search location");
        // TODO
    }

    swap(item: DetailedItem) {
        // Get the owner
        this.itemsService.getUser(item.owner_username)
            .then(
                owner => {
                    this.offerService.openOfferModal([this.user, owner, item]);
                    $("#send-proposition-modal").modal('show');
                },
                error => this.toastr.error("Can't get the owner", "Error")
            );
    }

    share(item: DetailedItem) {
        this.toastr.warning("for this '" + item.name + "' (TODO)", "Share item");
        // TODO
    }
}
