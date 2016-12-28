import {Component, OnInit, ViewEncapsulation, EventEmitter, Output} from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';

import {CropperSettings} from 'ng2-img-cropper';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { AuthService } from '../../shared/authentication/authentication.service';
import { UserCreationDTO } from './user-creation-dto';
import { UserLoginDTO } from './user-login-dto';

declare let $:any;

@Component({
    moduleId: module.id,
    selector: 'create-account-modal',
    encapsulation: ViewEncapsulation.None,
    styles: [`
        .result {
            margin-top: 30px;
            display: inline-block;
            padding: 1px;
            margin-left: auto;
            margin-right: auto;
            display: block;
        }

        .result.rounded > img {
            border-radius: 100px;
        }

        .pull-left {
            width: 100%;
            float: left;
            margin-right: 10px;
            padding: 10px;
            border: 1px solid rgba(0, 0, 0, 0.15);
            border-radius: 0.25rem;
        }
    `],
    templateUrl: './create-account-modal.component.html'
})

export class CreateAccountModalComponent implements OnInit {

    // EventEmitter to call login function of the ProfileComponent after registering
    @Output() myEvent = new EventEmitter();

    // Form fields
    private registerForm: FormGroup;
    private username = new FormControl("", Validators.required);
    private email = new FormControl("", Validators.required);
    private password = new FormControl("", Validators.required);
    private confirmPassword = new FormControl("", Validators.required);
    private firstName = new FormControl("", Validators.required);
    private lastName = new FormControl("", Validators.required);
    private address = new FormControl("", Validators.required);
    private region = new FormControl("", Validators.required);
    private country = new FormControl("", Validators.required);

    // profile picture
    data: any;
    cropperSettings: CropperSettings;
 
    constructor(private authService: AuthService,
                private formBuilder: FormBuilder,
                public toastr: ToastsManager) {
 
        this.cropperSettings = new CropperSettings();
        this.cropperSettings.width = 140;
        this.cropperSettings.height = 140;
        this.cropperSettings.keepAspect = false;

        this.cropperSettings.croppedWidth = 140;
        this.cropperSettings.croppedHeight = 140;

        this.cropperSettings.canvasWidth = 320;
        this.cropperSettings.canvasHeight = 300;

        this.cropperSettings.minWidth = 140;
        this.cropperSettings.minHeight = 140;

        this.cropperSettings.rounded = true;
        this.cropperSettings.minWithRelativeToResolution = false;

        this.cropperSettings.cropperDrawSettings.strokeColor = 'rgba(238, 213, 169, 1)';
        this.cropperSettings.cropperDrawSettings.strokeWidth = 2;

        this.data = {};
 
    }

    ngOnInit() {
        this.registerForm = this.formBuilder.group({
            username: this.username,
            email: this.email,
            password: this.password,
            confirmPassword: this.confirmPassword,
            address: this.address,
            region: this.region,
            country: this.country,
            firstName: this.firstName,
            lastName: this.lastName
        });
    }

    register() {
        let user = new UserCreationDTO(
            this.username.value,
            this.email.value,
            this.password.value,
            this.confirmPassword.value,
            this.firstName.value,
            this.lastName.value,
            this.address.value,
            this.region.value,
            this.country.value,
            this.data.image
        );

        if (user.password !== user.confirmPassword) {
            this.toastr.error('Password confirmation is different', 'Passwords don\'t match');
            this.password.reset();
            this.confirmPassword.reset();
        } else {
            this.authService.register(user).then(
                res => {
                    console.log(res);
                    if(res.status == 201) {
                        this.toastr.success('Account successfully created', 'Registration succeed!');
                        $('#create-user-modal').modal('hide');
                        let userLoginDTO = new UserLoginDTO(user.username, user.password);
                        console.log(userLoginDTO);
                        this.myEvent.emit(userLoginDTO);
                    }
                },
                error => this.toastr.error(error, 'Error')
            );
        }
        
    }
}
