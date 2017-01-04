import {Component, ViewEncapsulation, OnInit} from '@angular/core';

import { OfferService } from './offers.service';
import { ItemsService } from '../items/items.service';

import { User } from '../profile/user';
import { Owner } from '../items/owner';
import { DetailedItem } from '../items/detailed-item';

@Component({
    moduleId: module.id,
    selector: 'send-proposition-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './send-proposition-modal.component.html'
})
export class SendPropositionModalComponent implements OnInit {

    user: User;
    owner: Owner;
    item: DetailedItem;

    constructor(private offerService: OfferService,
                private itemsService: ItemsService) {
        offerService.offerModalSelected$.subscribe(
            offerArray => {
                this.initOffer(offerArray);
        });

        this.user = new User();
        this.owner = new Owner();
    }

    ngOnInit() {
    }

    // offerArray contains the offer elements where [0]=user, [1]=owner, [2]=item wanted
    initOffer(offerArray) {
        this.user = offerArray[0];
        this.owner = offerArray[1];
        this.item = offerArray[2];

        console.log(this.user);
        console.log(this.owner);
        console.log(this.item);



        // Get owner's inventory

        // Display first owner's inventory item as the item wanted

    }

    sendOffer() {
        // send the offer to the owner
        // TODO : which one is active ? the one who's class is "is-selected"

    }
}
