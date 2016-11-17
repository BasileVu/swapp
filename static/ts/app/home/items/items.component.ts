import {Component, ViewEncapsulation, OnInit} from '@angular/core';

import {ItemsService} from "./items.service";

// Add the RxJS Observable operators.
import {Item} from "./item";

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html'
})
export class ItemsComponent implements OnInit {

    errorMessage: string = "No items available for now";
    items: Item[];
    mode = 'Observable';
    constructor (private itemsService: ItemsService) {}

    ngOnInit() {
        this.getItems();
    }

    getItems() {
        this.itemsService.getItems()
            .then(
                items => this.items = items,
                error =>  this.errorMessage = <any>error);
    }
}
