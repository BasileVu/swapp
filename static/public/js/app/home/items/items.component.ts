import {Component, ViewEncapsulation, OnInit, OnChanges} from '@angular/core';

import { ItemsService } from './items.service';

import { DetailedItem } from './detailed-item';

declare var $:any;

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html'
})
export class ItemsComponent implements OnInit, OnChanges {

    errorMessage: string = "No items available for now";
    items: Array<DetailedItem>;
    selectedItem: DetailedItem;

    constructor (private itemsService: ItemsService) {}

    ngOnInit() {
        this.getItems();
        
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
                    this.items = items;
                },
                error =>  this.errorMessage = <any>error);
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
