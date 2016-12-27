import {Component, ViewEncapsulation, OnInit} from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';

import { AuthService } from '../../shared/authentication/authentication.service';
import { User } from './user';

@Component({
    moduleId: module.id,
    selector: 'profile',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile.component.html'
})

export class ProfileComponent implements OnInit {

    loggedIn: boolean;
    user: User;

    private loginForm: FormGroup;
    private loginName = new FormControl("", Validators.required);
    private loginPass = new FormControl("", Validators.required);

    constructor(private authService: AuthService,
                private formBuilder: FormBuilder) {}

    ngOnInit() {
        this.loggedIn = this.authService.isLoggedIn();

        this.loginForm = this.formBuilder.group({
            loginName: this.loginName,
            loginPass: this.loginPass
        });
    }

    login() {
        console.log("login " + this.loginName.value + " " + this.loginPass.value);
        //this.toastr.success("Welcome DamienRonchon !", "Login succeed");
        // TODO : for preview only
        //this.router.navigate(['./dashboard']);

        this.authService.login(this.loginName.value, this.loginPass.value).then(
            res => {
                this.loggedIn = true;
                console.log("Successfully logged in 1/2");
                this.authService.selectLoggedIn(this.loggedIn);
                console.log("Successfully logged in 2/2");
                // this.toastr.success("Welcome username !", "Login succeed");
            },
            error => console.log("error caca: "+error) // TODO : Toastr ? Message under form ?
        );
    }
}
