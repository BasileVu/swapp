import {
    Component, 
    ViewEncapsulation, 
    OnInit,
    trigger,
    state,
    style,
    transition,
    animate,
    Inject,
    Output,
    EventEmitter
} from '@angular/core';
import { DOCUMENT } from '@angular/platform-browser'
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';
import { Subscription }   from 'rxjs/Subscription';

import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { AuthService } from '../../shared/authentication/authentication.service';
import { User } from './user';

declare let $:any;
declare let google: any;

@Component({
    moduleId: module.id,
    selector: 'profile',

    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile.component.html',
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
    ]
})

export class ProfileComponent implements OnInit {

    // EventEmitter to call login function of the ProfileComponent after registering
    @Output() profilePictureEvent = new EventEmitter();

    loggedIn: boolean;
    subscription: Subscription;
    user: User;

    private loginForm: FormGroup;
    private loginName = new FormControl("", Validators.required);
    private loginPass = new FormControl("", Validators.required);

    private url: String;

    constructor(private authService: AuthService,
                private formBuilder: FormBuilder,
                @Inject(DOCUMENT) private document: any,
                public toastr: ToastsManager) {
                    this.url = this.document.location.href;
                    if (this.url.slice(-1) === '/') 
                        this.url = this.url.substr(0, this.url.length - 1);
                }

    ngOnInit() {
        this.user = new User();
        this.loggedIn = this.authService.isLoggedIn();

        this.loginForm = this.formBuilder.group({
            loginName: this.loginName,
            loginPass: this.loginPass
        });

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => this.loggedIn = loggedIn
        );
    }

    // $event is an object corresponding to an array with [0]=UserLoginDTO, [1]=true on account creation, false otherwise
    login($event) {
        this.authService.login($event[0]).then(
            res => {
                this.loggedIn = true;
                this.authService.selectLoggedIn(this.loggedIn);
                let accountOnCreation: boolean = $event[1];
                if (accountOnCreation) {
                    this.profilePictureEvent.emit();
                } else {
                    this.toastr.success("Welcome " + $event.username + " !", "Login succeed");
                    this.getAccount();

                    setTimeout(function(){
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

                        // open user edition modal /////////////////////
                        var openUpdateProfileButtons = $('.open-update-profile-modal');
                        var updateProfileModal = $('#update-user-modal');
                        openUpdateProfileButtons.each(function () {
                            $(this).click(function () {
                                updateProfileModal.modal('show');
                            });
                        });

                        // open user profile modal /////////////////////
                        var openProfileButtons = $('.open-profile-modal');
                        var profileModal = $('#user-profile-modal');
                        openProfileButtons.each(function () {
                            $(this).click(function () {
                                profileModal.modal('show');
                            });
                        });
                        profileModal.on('show.bs.modal', function (e) {
                            setTimeout(function () {
                                inventory.flickity('resize');

                                // profile map
                                var map = new google.maps.Map(document.getElementById('profile-map'), {
                                    center: {lat: -34.197, lng: 150.844},
                                    scrollwheel: false,
                                    zoom: 8
                                });
                                var marker = new google.maps.Marker({
                                    map: map,
                                    position: {lat: -34.197, lng: 150.844}
                                });
                                var infowindow = new google.maps.InfoWindow({
                                    content: '<h3 class="map-title">Adresse complète</h3>'
                                });
                                infowindow.open(map, marker);
                            }, 300)
                        });

                        // open notif modal /////////////////////
                        var openNotifButtons = $('.open-notif-modal');
                        var notifModal = $('#notification-modal');
                        openNotifButtons.each(function () {
                            $(this).click(function () {
                                notifModal.modal('show');
                            });
                        });

                        // open accept proposition modal /////////////////////
                        var openAcceptPropositionButtons = $('.open-accept-proposition-modal');
                        var acceptPropositionModal = $('#accept-proposition-modal');
                        openAcceptPropositionButtons.each(function () {
                            $(this).click(function () {
                                acceptPropositionModal.modal('show');
                            });
                        });
                    }, 100);
                }

            },
            error => this.toastr.error(error, "Error")
        );
    }

    getAccount() {
        this.authService.getAccount().then(
            user => {
                this.user = user;
                console.log(this.user);
                this.authService.selectUser(this.user);
            },
            error => this.toastr.error(error, "Error")
        );
    }
}
