import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";

@Component({
    moduleId: module.id,
    selector: 'profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile-modal.component.html'
})

export class ProfileModalComponent implements OnInit {

    private loggedIn: boolean;
    subscription: Subscription;

    constructor(private authService : AuthService) {}

    ngOnInit() {
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => this.loggedIn = loggedIn
        );
    }
}
