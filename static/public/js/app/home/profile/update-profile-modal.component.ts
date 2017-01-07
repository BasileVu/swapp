import {
    Component, OnInit, ViewEncapsulation, style,
    animate, transition, state, trigger, ViewChild, EventEmitter, Output
} from '@angular/core';
import {Validators, FormControl, FormGroup, FormBuilder} from "@angular/forms";
import {Subscription} from "rxjs";

import { ImageCropperComponent, CropperSettings} from 'ng2-img-cropper';
import {ToastsManager} from "ng2-toastr/ng2-toastr";

import {Category} from "../search/category";
import {SearchService} from "../search/search.service";
import {Account} from "./account";
import {AuthService} from "../../shared/authentication/authentication.service";
import {ProfileService} from "./profile.service";

@Component({
    moduleId: module.id,
    selector: 'update-profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './update-profile-modal.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({opacity: 1, transform: 'translateX(0)'})),
            transition('void => *', [
                style({
                    opacity: 0,
                    transform: 'translateX(-100%)'
                }),
                animate('0.2s ease-in')
            ]),
            transition('* => void', [
                animate('0.2s 10 ease-out', style({
                    opacity: 0,
                    transform: 'translateX(100%)'
                }))
            ])
        ])
    ],
    styles:[`
        .category-choice {
            margin:4px;
            background-color:#EFEFEF;
            border-radius:4px;
            border:1px solid #D0D0D0;
            overflow:auto;
            float:left;
        }
        
        .category-choice label {
            float:left;
            width:4.0em;
        }
        
        .category-choice label span {
            text-align:center;
            padding:3px 0px;
            display:block;
        }
        
        .category-choice label input {
            position:absolute;
            display: none;
        }
        
        .category-choice input:checked + span {
            background-color:#911;
            color:#fff;
        }
    `]
})

export class UpdateProfileModalComponent implements OnInit {

    interests: Array<number> = []; // The category ids in which the user is interested in
    categories: Array<Category> = [];
    subscription: Subscription;
    account: Account = new Account();

    @Output() updateAccountEvent = new EventEmitter();

    // Form fields
    private updateForm: FormGroup;
    private username = new FormControl("", Validators.required);
    private email = new FormControl("", Validators.required);
    private password = new FormControl();
    private confirmPassword = new FormControl();
    private firstName = new FormControl("", Validators.required);
    private lastName = new FormControl("", Validators.required);
    private street = new FormControl("", Validators.required);
    private city = new FormControl("", Validators.required);
    private region = new FormControl("", Validators.required);
    private country = new FormControl("", Validators.required);

    // profile picture
    data: any;
    cropperSettings: CropperSettings;
    @ViewChild('cropper', undefined)
    cropper:ImageCropperComponent;
    private file:File;

    constructor(private searchService: SearchService,
                private formBuilder: FormBuilder,
                private authService: AuthService,
                private profileService: ProfileService,
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

        this.cropperSettings.noFileInput = true;

        this.data = {};
    }

    ngOnInit() {
        // Build the form
        this.updateForm = this.formBuilder.group({
            username: this.username,
            email: this.email,
            password: this.password,
            confirmPassword: this.confirmPassword,
            street: this.street,
            city: this.city,
            region: this.region,
            country: this.country,
            firstName: this.firstName,
            lastName: this.lastName
        });

        // Get categories
        this.searchService.getCategories().then(
            categories => this.categories = categories,
            error => this.toastr.error("Can't get categories", "Error")
        );

        // Subscribe to login event to get user when he logs in
        this.subscription = this.authService.accountSelected$.subscribe(
            account => {
                this.account = account;

                this.data.image = this.account.profile_picture_url;
                this.username.setValue(this.account.username);
                this.email.setValue(this.account.email);
                this.street.setValue(this.account.location.street);
                this.city.setValue(this.account.location.city);
                this.region.setValue(this.account.location.region);
                this.country.setValue(this.account.location.country);
                this.firstName.setValue(this.account.first_name);
                this.lastName.setValue(this.account.last_name);

                console.log(this.data);
            }
        );
    }

    // Add or remove a category interest if selected/unselected
    updateCheckbox(deliverymethod_id: number, checked: boolean) {
        if (checked) {
            this.interests.push(+deliverymethod_id);
        } else {
            let index = this.interests.indexOf(+deliverymethod_id, 0);
            if (index > -1) {
                this.interests.splice(index, 1);
            }
        }
    }

    update() {
        // Verifications

        // Upload profile
    }

    fileChangeListener($event: any) {
        const image: any = new Image();
        this.file = $event.target.files[0];
        const myReader: FileReader = new FileReader();
        const that = this;
        myReader.onloadend = function (loadEvent:any) {
            image.src = loadEvent.target.result;
            that.cropper.setImage(image);
        };

        myReader.readAsDataURL(this.file);
    }

    addProfilePicture() {
        if (this.data.image != undefined) {
            let formData:FormData = new FormData();
            formData.append('image', this.file, this.file.name);
            formData.append('user', 10); // 10 is an arbitrary value, we just need to indicate that user has a value
            this.profileService.addImage(formData)
                .then( // now signal the ProfileComponent that we uploaded picture
                    res => this.updateAccountEvent.emit(),
                    error => this.updateAccountEvent.emit()
                );
        }
    }

}
