import {Component, ViewEncapsulation, OnInit, Input} from '@angular/core';

import { OfferService } from './offers.service';
import { ItemsService } from '../items/items.service';

import { User } from '../profile/user';
import { DetailedItem } from '../items/detailed-item';

@Component({
    moduleId: module.id,
    selector: 'send-proposition-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './send-proposition-modal.component.html'
})
export class SendPropositionModalComponent implements OnInit {

    user: User;
    owner: User;
    item: DetailedItem;

    constructor(private offerService: OfferService,
                private itemsService: ItemsService) {
        offerService.offerModalSelected$.subscribe(
            offerArray => {
                this.initOffer(offerArray);
        });

        this.user = new User();
        this.owner = new User();
    }

    ngOnInit() {
    }

    // offerArray contains the offer elements where [0]=user (type User), [1]=owner (type User), [2]=item wanted (type DetailedItem)
    initOffer(offerArray) {
        this.user = offerArray[0];
        this.owner = offerArray[1];
        this.item = offerArray[2];

        console.log(this.user);
        console.log(this.owner);
        console.log(this.item);

        // Display first owner's inventory item as the item wanted

        /*
        setTimeout(function(){
            // swapp inventories /////////////////////////
            $('.swapp-inventory-mine').flickity({
                // options
                cellAlign: 'center',
                contain: true,
                imagesLoaded: true,
                wrapAround: true,
                groupCells: '100%',
                prevNextButtons: false,
                adaptiveHeight: true,
                pageDots: true
            });
            $('.swapp-inventory-yours').flickity({
                // options
                cellAlign: 'center',
                contain: true,
                imagesLoaded: true,
                wrapAround: true,
                groupCells: '100%',
                prevNextButtons: false,
                adaptiveHeight: true,
                pageDots: true
            });

            console.log("fully loaded after 600ms");
        }, 600);
        */
    }

    sendOffer() {
        // send the offer to the owner
        // TODO : which one is active ? the one who's class is "is-selected"

    }
}
