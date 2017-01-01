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
    private counter: number = 1;

    private inventory: Array<InventoryItem> = new Array();
    
    constructor(private authService: AuthService, private itemsService: ItemsService) {
        console.log("constructor " + ++this.counter);
     }

    ngOnInit(): void {
        this.loggedIn = this.authService.isLoggedIn();
    }

    ngOnChanges() {
        if (this.loggedIn && this.inventory.length === 0) {
            this.authService.getAccount().then(
                user => {
                    for(let i in user.items){
                        this.itemsService.getItem(user.items[i]).then(
                            item => {
                                let image: string = undefined;
                                if (item.image_set != undefined)
                                    image = item.image_set[0];

                                let inventoryItem = new InventoryItem(item.id, item.name, image, item.creation_date);
                                this.inventory.push(inventoryItem);
                                console.log("end get");

                            },
                            error => console.log(error)
                        ).then(function() {
                            // home inventory /////// ////////////////////
                            $('.home-inventory').flickity({
                                // options
                                cellAlign: 'center',
                                contain: true,
                                imagesLoaded: true,
                                wrapAround: true,
                                groupCells: '100%',
                                prevNextButtons: false,
                                adaptiveHeight: true
                            });
                        });
                    }

                    console.log("for end");

                    setTimeout(function(){
                        

                        // open item creation modal /////////////////////
                        $('.open-new-item-modal').each(function () {
                            $(this).click(function () {
                                $('#add-item-modal').modal('show');
                            });
                        });
                        console.log("finito");

                    },1000)
                    
                },
                error => console.log(error)
            ).then(function() {
                
            });
        }
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

    gotoDetail(item_id: number): void {
        console.log("clicked. item_id: " + item_id);

        let service = this.itemsService;
        service.getItem(item_id)
            .then(
                item => {
                    service.selectItem(item);
                },
                error => console.log(error));

        /*
        service.getOwner(owner_id)
            .then(
                owner => {
                    service.selectOwner(owner);
                },
                error => console.log(error));
                */

        service.getComments(item_id)
            .then(
                comments => {
                    service.selectComments(comments);
                },
                error => console.log(error));
    }

    updateInventoryDisplay(): void {
        // home inventory /////// ////////////////////
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

        console.log("end js");
    }
}
