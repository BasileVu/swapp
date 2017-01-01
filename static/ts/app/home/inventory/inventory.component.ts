import {
    Component, 
    Input, 
    ViewEncapsulation, 
    OnInit, 
    OnChanges,
    trigger,
    state,
    style,
    transition,
    animate,
} from '@angular/core';

import { AuthService } from '../../shared/authentication/authentication.service';
import { InventoryItem } from './inventory-item';
import { ItemsService } from '../items/items.service';
import {Item} from "../items/item";
import {Owner} from "../items/owner";

declare var $:any;

@Component({
    moduleId: module.id,
    selector: 'inventory',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './inventory.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({opacity: 1, transform: 'translateX(0)'})),
            transition('void => *', [
                style({
                    opacity: 0,
                    transform: 'translateX(0) scale(0)'
                }),
                animate(200)
            ]),
            transition('* => void', [
                animate(200, style({
                    opacity: 0,
                    transform: 'translateX(0) scale(0)'
                }))
            ])
        ])
    ]
})
export class InventoryComponent implements OnInit, OnChanges {

    @Input() loggedIn: boolean;

    private inventory: Array<InventoryItem> = new Array();
    
    constructor(private authService: AuthService, private itemsService: ItemsService) { }

    ngOnInit(): void {
        this.loggedIn = this.authService.isLoggedIn();
    }

    ngOnChanges() {

        // settimeout is an hack to have the inventory displayed nicely.
        // It's probably due to the DOM elements which are not fully loaded
        // on ngOnChanges so we wait a little time (100ms)
        setTimeout(function() {
            // home inventory ///////////////////////////
            var inventory = $('.home-inventory').flickity({
                // options
                cellAlign: 'center',
                contain: true,
                imagesLoaded: true,
                wrapAround: true,
                groupCells: '100%',
                prevNextButtons: false,
                adaptiveHeight: true
            });

            // open item creation modal /////////////////////
            var addItemButtons = $('.open-new-item-modal');
            var newItemModal = $('#add-item-modal');
            addItemButtons.each(function () {
                $(this).click(function () {
                    newItemModal.modal('show');
                });
            });

            if(this.loggedIn) {
                this.authService.getAccount().then(
                    user => {
                        for (let i in user.items) {
                            this.itemsService.getItem(user.items[i]).then(
                                item => {
                                    this.inventory.push(item);
                                },
                                error => console.log(error)
                            );
                        }
                    },
                    error => console.log(error)
                );
            }
        }, 100);
    }

    // We receive an ItemCreationDTO object so we'll change it into an InventoryItem
    addItemEvent($event) {
        let inventoryItem = new InventoryItem(
            $event.url,
            $event.name, 
            $event.images[0], 
            $event.creation_date);
        
        this.inventory.push(inventoryItem);

        console.log("inventory:");
        console.log(this.inventory);
    }

    gotoDetail(item_id: number, owner_id: number): void {
        console.log("clicked. item_id: " + item_id + " owner_id: " + owner_id);

        let service = this.itemsService;
        service.getItem(item_id)
            .then(
                item => {
                    service.selectItem(item);
                },
                error => console.log(error));

        service.getOwner(owner_id)
            .then(
                owner => {
                    service.selectOwner(owner);
                },
                error => console.log(error));

        service.getComments(item_id)
            .then(
                comments => {
                    service.selectComments(comments);
                },
                error => console.log(error));
    }
}
