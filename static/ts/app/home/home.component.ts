import {Component, ViewEncapsulation, OnInit, AfterViewInit } from '@angular/core';

import { AuthService } from '../shared/authentication/authentication.service';
import {ItemsService} from "./items/items.service";

@Component({
    moduleId: module.id,
    selector: 'home',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './home.component.html',
    providers: [ItemsService]
})

export class HomeComponent implements OnInit, AfterViewInit {

    hidden: boolean;

    constructor(private authService : AuthService, private itemsService: ItemsService){}

    ngOnInit() {
        this.hidden = !this.authService.checkCredentials();
    }

    ngAfterViewInit() {
    }
}
