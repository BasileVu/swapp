import {Component, ViewEncapsulation, OnInit, AfterViewInit } from '@angular/core';

import { AuthService } from '../shared/authentication/authentication.service';
import {ItemsService} from "./items/items.service";
import { Subscription }   from 'rxjs/Subscription';

@Component({
    moduleId: module.id,
    selector: 'home',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './home.component.html',
    providers: [ItemsService]
})

export class HomeComponent implements OnInit, AfterViewInit {

    private loggedIn: boolean;
    subscription: Subscription;
 
    constructor(private authService : AuthService) { }

    ngOnInit() {
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => this.loggedIn = loggedIn
        );
    }

    ngAfterViewInit() {
    }
}
