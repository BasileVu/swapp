import {Component, ViewEncapsulation, OnInit} from '@angular/core';

import { ItemsService } from "./items.service";

import { Item } from "./item";
import {Subscription} from "rxjs";

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html',
    providers: []
})
export class ItemsComponent implements OnInit {

    errorMessage: string = "No items available for now";
    items: Array<Item>;
    selectedItem: Item;

    constructor (private itemsService: ItemsService) {}

    ngOnInit() {
        this.getItems();
        this.itemsService.getItemsSubject().subscribe((items: Item[]) => {
            this.items = items;
        });
    }

    getItems() {
        this.itemsService.getItems()
            .then(
                items => this.items = items,
                error =>  this.errorMessage = <any>error);
    }

    gotoDetail(id: number): void {
        console.log("clicked. id: " + id);

        let service = this.itemsService;
        service.getItem(id)
            .then(
                item => {
                    this.selectedItem = item;
                    service.selectItem(this.selectedItem)
                },
                error => this.errorMessage = <any>error);
    }
}
