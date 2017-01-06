import {
    Component, ViewEncapsulation, OnInit
} from '@angular/core';

import { OfferService } from './offers.service';

import { User } from '../profile/user';
import { DetailedItem } from '../items/detailed-item';
import { Offer } from "./offer";
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

declare let $:any;

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
    ownerItems: Array<any>;
    currentUserItem: DetailedItem;
    currentOwnerItem: DetailedItem;
    firstTime = true;

    constructor(private offerService: OfferService,
                public toastr: ToastsManager) {
        offerService.offerModalSelected$.subscribe(
            offerArray => {
                this.initOffer(offerArray);
            });

        this.user = new User();
        this.ownerItems = [];
        this.owner = new User();
    }

    ngOnInit() {
        var sendPropositionModal = $('#send-proposition-modal');
        sendPropositionModal.on('hide.bs.modal', function (e: any) {
            $('.swapp-inventory-mine').flickity('destroy');
            $('.swapp-inventory-yours').flickity('destroy');
        });

    }

    // offerArray contains the offer elements where [0]=user (type User), [1]=owner (type User), [2]=item wanted (type DetailedItem)
    // We clone the owner every item because he's always different (a simple copy of object is a copy by reference)
    initOffer(offerArray: Array<any>) {
        this.owner = this.offerService.cloneUser(offerArray[1]);
        this.item = offerArray[2];
        this.ownerItems = new Array<any>(this.owner.items.length);
        let i = 1;
        for (let ownerItem of this.owner.items)
            if (ownerItem.id === this.item.id)
                this.ownerItems[0] = ownerItem;
            else
                this.ownerItems[i++] = ownerItem;

        this.user = this.offerService.cloneUser(offerArray[0]);
    }

    sendOffer() {
        // send the offer to the owner
        // TODO : which one is active ? the one who's class is "is-selected"

        // get instance
        var mineflkty = $('.swapp-inventory-mine').data('flickity');
        // access properties
        let userItem = this.user.items[mineflkty.selectedIndex];

        // get instance
        var yourflkty = $('.swapp-inventory-yours').data('flickity');
        // access properties
        let ownerItem = this.ownerItems[yourflkty.selectedIndex];

        let offer: Offer = new Offer();
        offer.item_given = userItem.id;
        offer.item_received = ownerItem.id;
        let ownerFullname = this.owner.first_name + " " + this.owner.last_name;
        offer.comment = "Hello " + ownerFullname + ". I would like to propose you my " +
            userItem.name + " for your " + ownerItem.name + ".";

        this.offerService.sendOffer(offer).then(
            res => this.toastr.success("to " + ownerFullname, "Offer sent"),
            error => this.toastr.error(error, "Error")
        );
    }
}
