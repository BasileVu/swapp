import {Component, ViewEncapsulation, OnInit, AfterViewInit } from '@angular/core';
import {Observable} from 'rxjs';

import { AuthService } from '../shared/authentication/authentication.service';

@Component({
    moduleId: module.id,
    selector: 'home',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './home.component.html'
})

export class HomeComponent implements OnInit, AfterViewInit {

    hidden: boolean;

    constructor(private authService : AuthService){}

    ngOnInit() {
        this.hidden = !this.authService.checkCredentials();
    }

    ngAfterViewInit() {
    }
}
