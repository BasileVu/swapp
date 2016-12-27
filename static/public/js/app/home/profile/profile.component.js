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
        }, function (error) { return console.log("error caca: " + error); } // TODO : Toastr ? Message under form ?
        );
    };
    ProfileComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'profile',
            encapsulation: core_1.ViewEncapsulation.None,
            templateUrl: './profile.component.html'
        }), 
        __metadata('design:paramtypes', [authentication_service_1.AuthService, forms_1.FormBuilder])
    ], ProfileComponent);
    return ProfileComponent;
}());
exports.ProfileComponent = ProfileComponent;
//# sourceMappingURL=profile.component.js.map