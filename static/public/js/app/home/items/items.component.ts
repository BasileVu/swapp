import {Component, ViewEncapsulation, OnInit, OnChanges} from '@angular/core';

import { ItemsService } from './items.service';

import { DetailedItem } from './detailed-item';
import { Item } from './item';
import { Owner } from './owner';
import { Comment } from './comment';
import {Subscription} from 'rxjs';

declare var $:any;

@Component({
    moduleId: module.id,
    selector: 'items',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items.component.html',
    providers: []
})
export class ItemsComponent implements OnInit, OnChanges {

    errorMessage: string = "No items available for now";
    items: Array<Item>;
    selectedItem: DetailedItem;
    selectedOwner: Owner;
    selectedComments: Array<Comment>;

    constructor (private itemsService: ItemsService) {}

    ngOnInit() {
        this.getItems();
        
        this.itemsService.getItemsSubject().subscribe((items: Item[]) => {
            this.items = items;

            setTimeout(function(){
                $('.grid').isotope({
                    // options
                    itemSelector: '.grid-item',
                    layoutMode: 'masonry'
                });
                // layout only when images are loaded
                $('.grid').imagesLoaded().progress( function() {
                    $('.grid').isotope('layout');
                });
                // display items details when hovered
                $('.grid-item').hover(function () {
                    $(this).addClass('hovered');
                    $('.grid').isotope('layout');
                }, function () {
                    $(this).removeClass('hovered');
                    $('.grid').isotope('layout');
                });
                
                $('.open-modal-item-x').click(function () {
                    $('#view-item-x').modal('show');
                });
            }, 100);
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

    gotoDetail(item_id: number, owner_id: number): void {
        console.log("clicked. item_id: " + item_id);

        let service = this.itemsService;
        service.getDetailedItem(item_id)
            .then(
                item => {
                    this.selectedItem = item;
                    service.selectItem(this.selectedItem);

                    setTimeout(function(){
                $('.grid').isotope({
                    // options
                    itemSelector: '.grid-item',
                    layoutMode: 'masonry'
                });
                // layout only when images are loaded
                $('.grid').imagesLoaded().progress( function() {
                    $('.grid').isotope('layout');
                });
                // display items details when hovered
                $('.grid-item').hover(function () {
                    $(this).addClass('hovered');
                    $('.grid').isotope('layout');
                }, function () {
                    $(this).removeClass('hovered');
                    $('.grid').isotope('layout');
                });
            }, 200);
                },
                error => this.errorMessage = <any>error);
    }

    searchCategory(category_id: number) {
        console.log("category id: " + category_id);
        // TODO
    }
}
