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
import {
    Account, AccountUpdateDTO, PasswordUpdateDTO,
    LocationDTO
} from "./account";
import {AuthService} from "../../shared/authentication/authentication.service";
import {ProfileService} from "./profile.service";
import {UserLoginDTO} from "./user-login-dto";

class CategoryDesired {
    category: Category;
    desired: boolean;

    constructor(category: Category, desired: boolean) {
        this.category = category;
        this.desired = desired;
    }
}

declare let $: any;

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
            width: 100%;
            margin-bottom: 0;
        }
        
        .category-choice label span {
            text-align:center;
            padding:3px 10px 3px 10px;
            display:block;
        }
        
        .category-choice label input {
            position:absolute;
            display: none;
        }
        
        .category-choice input:checked + span {
            background-color:#5fba4b;
            color:#fff;
        }
    `]
})

export class UpdateProfileModalComponent implements OnInit {

    interests: Array<number> = []; // The category in which the user is interested in
    categories: Array<CategoryDesired> = [];
    subscription: Subscription;
    account: Account = new Account();

    @Output() updateAccountEvent = new EventEmitter();

    // Form fields
    private updateForm: FormGroup;
    private username = new FormControl("", Validators.required);
    private email = new FormControl("", Validators.required);
    private oldPassword = new FormControl();
    private newPassword = new FormControl();
    private confirmNewPassword = new FormControl();
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
    pictureChanged = false;

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
            oldPassword: this.oldPassword,
            newPassword: this.newPassword,
            confirmNewPassword: this.confirmNewPassword,
            street: this.street,
            city: this.city,
            region: this.region,
            country: this.country,
            firstName: this.firstName,
            lastName: this.lastName
        });

        // Get categories
        this.searchService.getCategories().then(
            categories => {
                for (let c of categories)
                    this.categories.push(new CategoryDesired(c, false));
            },
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

                // Check categories already desired by user
                for (let c of this.categories)
                    for (let ac of this.account.categories)
                        if (c.category.id === ac.id) {
                            c.desired = true;
                            this.interests.push(c.category.id);
                        }
            }
        );

        let that = this;
        $('#update-user-modal').on('hide.bs.modal', function (e: any) {
            that.interests = [];
            for (let category of that.account.categories)
                that.interests.push(category.id);

            that.newPassword.reset();
            that.oldPassword.reset();
            that.confirmNewPassword.reset();
        });
    }

    // Add or remove a category interest if selected/unselected
    updateCheckbox(category_id: number, checked: boolean) {
        if (checked) {
            this.interests.push(+category_id);
        } else {
            let index = this.interests.indexOf(+category_id, 0);
            if (index > -1) {
                this.interests.splice(index, 1);
            }
        }
    }

    updateProfilePicture() {
        // upload profile picture if changed
        if (this.pictureChanged) {
            let formData:FormData = new FormData();
            formData.append('image', this.file, this.file.name);
            this.profileService.addProfilePicture(formData)
                .then( // now signal the ProfileComponent that we uploaded picture
                    res => {
                        this.toastr.success("", "Image uploaded");
                        this.updateAccountEvent.emit();
                    },
                    error => {
                        this.toastr.error(error, "Error");
                        this.updateAccountEvent.emit();
                    }
                );
        }
    }

    updatePassword() {
        // upload password if changed
        if (this.newPassword.value) {
            if(this.newPassword.value != this.confirmNewPassword.value) {
                this.toastr.error("New password don't match with confirmation", "Error");
            } else {
                // upload
                let passwordUpdateDTO = new PasswordUpdateDTO(this.oldPassword.value, this.newPassword.value);
                this.profileService.updatePassword(passwordUpdateDTO).then(
                    res => {
                        this.toastr.success("", "Password updated");
                        this.authService.login(new UserLoginDTO(this.account.username, this.newPassword.value)).then(
                            res => this.updateAccountEvent.emit(),
                            error => this.toastr.error(error, "Error")
                        );

                    },
                    error =>  {
                        this.toastr.error(error, "Error");
                    }
                );
            }
        }
    }

    updateLocation() {
        // upload location if changed
        if (this.city.value != this.account.location.city
            || this.region.value != this.account.location.region
            || this.street.value != this.account.location.street
            || this.country.value != this.account.location.country) {
            let location = new LocationDTO(this.street.value, this.city.value, this.region.value, this.country.value);
            this.profileService.updateLocation(location).then(
                res => {
                    this.toastr.success("", "Location updated");
                    this.updateAccountEvent.emit();
                },
                error => {
                    this.toastr.error(error, "Error");
                }
            );

        }
    }

    updateProfile() {
        // upload profile if changed
        if (this.username.value != this.account.username
            || this.firstName.value != this.account.first_name
            || this.lastName.value != this.account.last_name
            || this.email.value != this.account.email) {
            let accountUpdateDTO = new AccountUpdateDTO(this.username.value, this.firstName.value, this.lastName.value, this.email.value);
            this.profileService.updateAccount(accountUpdateDTO).then(
                res => {
                    this.toastr.success("", "Profile updated");
                    this.updateAccountEvent.emit();
                },
                error => {
                    this.toastr.error(error, "Error");
                }
            );
        }
    }

    updateCategories()  {
        let doUpdate = false;

        let accountCategories: Array<number> = [];
        for (let c of this.account.categories)
            accountCategories.push(c.id);

        for (let interest of this.interests)
            if (accountCategories.indexOf(interest, 0) < 0) {
                doUpdate = true;
                break;
            }

        if (!doUpdate) {
            for (let category of accountCategories)
                if (this.interests.indexOf(category, 0) < 0) {
                    doUpdate = true;
                    break;
                }
        }

        if (doUpdate) {
            let obj = {"interested_by": this.interests};
            this.profileService.updateCategories(obj).then(
                res => {
                    this.toastr.success("", "Interests updated");
                    this.updateAccountEvent.emit();
                },
                error => {
                    this.toastr.error(error, "Error");
                }
            );
        }
    }

    updateAccount() {
        this.updateProfilePicture();
        this.updateProfile();
        this.updateLocation();
        this.updatePassword();
        this.updateCategories();
    }

    fileChangeListener($event: any) {
        this.pictureChanged = true;
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
}
