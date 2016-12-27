import {
    Component, Input, ViewEncapsulation, OnInit, OnChanges
} from '@angular/core';

import { AuthService } from '../../shared/authentication/authentication.service';

declare var $:any;

@Component({
    moduleId: module.id,
    selector: 'inventory',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './inventory.component.html'
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
        }, 100);
    }
}
