import {
    Component, ViewEncapsulation, OnInit, style, animate, transition, state,
    trigger
} from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';

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
    templateUrl: './send-proposition-modal.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({transform: 'translateX(0) scale(1.1)'})),
            transition('void => *', [
                style({transform: 'translateX(0) scale(0)'}),
                animate('0.2s ease-in')
            ]),
            transition('* => void', [
                animate('0.2s 10 ease-out', style({transform: 'translateX(0) scale(0)'}))
            ])
        ])
    ]
})
export class SendPropositionModalComponent implements OnInit {

    user: User;
    owner: User;
    item: DetailedItem;
    ownerItems: Array<any>;
    displayMessage: boolean = false;

    // Form fields
    private offerForm: FormGroup;
    private message = new FormControl("", Validators.required);

    constructor(private offerService: OfferService,
                private formBuilder: FormBuilder,
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
        let sendPropositionModal = $('#send-proposition-modal');
        let that = this;
        sendPropositionModal.on('hide.bs.modal', function (e: any) {
            that.displayMessage = false;
            $('.swapp-inventory-mine').flickity('destroy');
            $('.swapp-inventory-yours').flickity('destroy');
        });

        // Initiate the comment form
        this.offerForm = this.formBuilder.group({
            message: this.message
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


    // display a form to fill the private message and a validation button
    validOffer() {

        // get instance
        let mineflkty = $('.swapp-inventory-mine').data('flickity');
        let yourflkty = $('.swapp-inventory-yours').data('flickity');

        let ownerFullname = this.owner.first_name + " " + this.owner.last_name;
        this.message.setValue("Hello " + ownerFullname + ". I would like to propose you this offer !");

        this.displayMessage = true;
    }

    // Send the offer to the owner
    sendOffer() {

        // get instance
        let mineflkty = $('.swapp-inventory-mine').data('flickity');
        // access properties
        let userItem = this.user.items[mineflkty.selectedIndex];

        // get instance
        let yourflkty = $('.swapp-inventory-yours').data('flickity');
        // access properties
        let ownerItem = this.ownerItems[yourflkty.selectedIndex];

        let ownerFullname = this.owner.first_name + " " + this.owner.last_name;

        let offer: Offer = new Offer();
        offer.item_given = userItem.id;
        offer.item_received = ownerItem.id;
        offer.comment = this.message.value;

        this.offerService.sendOffer(offer).then(
            res => this.toastr.success("to " + ownerFullname, "Offer sent"),
            error => {
                this.toastr.error(error, "Error");
                this.displayMessage = false;
            }
        );
    }
}
