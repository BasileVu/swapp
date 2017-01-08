import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";
import {Account} from "./account";

@Component({
    moduleId: module.id,
    selector: 'profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile-modal.component.html'
})

export class ProfileModalComponent implements OnInit {

    private loggedIn: boolean;
    user: Account;
    subscription: Subscription;

    constructor(private authService : AuthService) {}

    ngOnInit() {
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => this.loggedIn = loggedIn
        );
        this.authService.getAccount().then(
            account => {
                this.user = account;
                console.log(account);
            }
        );
    }
}
