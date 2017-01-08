import {Component, ViewEncapsulation, OnInit} from '@angular/core';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { ItemsService } from './items.service';

import { DetailedItem } from './detailed-item';
import {Subscription} from "rxjs";
import {AuthService} from "../../shared/authentication/authentication.service";

export let $: any;

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html'
})
export class ItemsComponent implements OnInit {

    items: Array<DetailedItem>;
    loggedIn: boolean;
    subscription: Subscription;
    infoMessage: string = "Loading items...";

    constructor (private itemsService: ItemsService,
                 private authService: AuthService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        this.items = [];

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                this.loggedIn = loggedIn;
                this.getItems();
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
                    this.items = items;
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
        console.log("category id: " + category_id);
        // TODO
    }
}
