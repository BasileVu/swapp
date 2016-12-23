import {Component, ViewEncapsulation, OnInit} from '@angular/core';

import { ItemsService } from "./items.service";

import { Item } from "./item";
import {Subscription} from "rxjs";

declare var $:any;

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
            //grid.arrange();
            // home grid ///////////////////////////
            var grid = $('.grid').isotope({
                // options
                itemSelector: '.grid-item',
                layoutMode: 'masonry'
            });
            // layout only when images are loaded
            grid.imagesLoaded().progress( function() {
                grid.isotope('layout');
            });
            // display items details when hovered
            $('.grid-item').hover(function () {
                $(this).addClass('hovered');
                grid.isotope('layout');
            }, function () {
                $(this).removeClass('hovered');
                grid.isotope('layout');
            });
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
