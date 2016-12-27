"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var forms_1 = require('@angular/forms');
var authentication_service_1 = require('../../shared/authentication/authentication.service');
var ProfileComponent = (function () {
    function ProfileComponent(authService, formBuilder) {
        this.authService = authService;
        this.formBuilder = formBuilder;
        this.loginName = new forms_1.FormControl("", forms_1.Validators.required);
        this.loginPass = new forms_1.FormControl("", forms_1.Validators.required);
    }
    ProfileComponent.prototype.ngOnInit = function () {
        this.loggedIn = this.authService.isLoggedIn();
        this.loginForm = this.formBuilder.group({
            loginName: this.loginName,
            loginPass: this.loginPass
        });
    };
    ProfileComponent.prototype.login = function () {
        var _this = this;
        console.log("login " + this.loginName.value + " " + this.loginPass.value);
        //this.toastr.success("Welcome DamienRonchon !", "Login succeed");
        // TODO : for preview only
        //this.router.navigate(['./dashboard']);
        this.authService.login(this.loginName.value, this.loginPass.value).then(function (res) {
            _this.loggedIn = true;
            console.log("Successfully logged in 1/2");
            _this.authService.selectLoggedIn(_this.loggedIn);
            console.log("Successfully logged in 2/2");
            // this.toastr.success("Welcome username !", "Login succeed");
            setTimeout(function () {
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
                            center: { lat: -34.197, lng: 150.844 },
                            scrollwheel: false,
                            zoom: 8
                        });
                        var marker = new google.maps.Marker({
                            map: map,
                            position: { lat: -34.197, lng: 150.844 }
                        });
                        var infowindow = new google.maps.InfoWindow({
                            content: '<h3 class="map-title">Adresse complète</h3>'
                        });
                        infowindow.open(map, marker);
                    }, 300);
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
        }, function (error) { return console.log("error caca: " + error); } // TODO : Toastr ? Message under form ?
        );
    };
    ProfileComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'profile',
            encapsulation: core_1.ViewEncapsulation.None,
            templateUrl: './profile.component.html',
            animations: [
                core_1.trigger('flyInOut', [
                    core_1.state('in', core_1.style({ opacity: 1, transform: 'translateX(0)' })),
                    core_1.transition('void => *', [
                        core_1.style({
                            opacity: 0,
                            transform: 'translateX(-100%)'
                        }),
                        core_1.animate('0.2s ease-in')
                    ]),
                    core_1.transition('* => void', [
                        core_1.animate('0.2s 10 ease-out', core_1.style({
                            opacity: 0,
                            transform: 'translateX(100%)'
                        }))
                    ])
                ])
            ]
        }), 
        __metadata('design:paramtypes', [authentication_service_1.AuthService, forms_1.FormBuilder])
    ], ProfileComponent);
    return ProfileComponent;
}());
exports.ProfileComponent = ProfileComponent;
//# sourceMappingURL=profile.component.js.map