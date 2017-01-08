import {Component, ViewEncapsulation, OnInit, OnChanges} from '@angular/core';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { ItemsService } from './items.service';

import { DetailedItem } from './detailed-item';
import {Subscription} from "rxjs";
import {AuthService} from "../../shared/authentication/authentication.service";
import {Category} from "../search/category";

export let $: any;

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html'
})
export class ItemsComponent implements OnInit, OnChanges {

    items: Array<DetailedItem>;
    loggedIn: boolean;
    subscription: Subscription;

    constructor (private itemsService: ItemsService,
                 private authService: AuthService,
                 public toastr: ToastsManager) {}

    ngOnInit() {
        this.items = [];
        this.getItems();

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                this.loggedIn = loggedIn;

                // Get other items when user is logged in
                // TODO : but the grid's display is breaking (see isotope library)
                // this.getItems();
            }
        );

        this.itemsService.getItemsSubject().subscribe((items: DetailedItem[]) => {
            this.items = items;
        });
    }

    ngOnChanges() {
        console.log("changes");
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
        console.log("category id: " + category_id);
        // TODO
    }
}
