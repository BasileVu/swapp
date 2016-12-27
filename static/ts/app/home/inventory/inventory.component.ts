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
    
    constructor(private authService: AuthService) { }

    ngOnInit(): void {
        this.loggedIn = this.authService.isLoggedIn();
    }

    ngOnChanges() {
        console.log("change loggedIn=" + this.loggedIn);

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
        }, 100);
    }
}
