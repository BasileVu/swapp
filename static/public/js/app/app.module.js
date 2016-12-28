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
var core_1 = require("@angular/core");
var platform_browser_1 = require("@angular/platform-browser");
var http_1 = require("@angular/http");
/* App Root */
var app_component_1 = require("./app.component");
var home_module_1 = require("./home/home.module");
/* Feature Modules */
var core_module_1 = require("./core/core.module");
var authentication_service_1 = require("./shared/authentication/authentication.service");
var ng2_toastr_1 = require("ng2-toastr/ng2-toastr");
/* Routing Module */
var app_routing_module_1 = require("./app-routing.module");
// Declare the NgModule decorator
var AppModule = (function () {
    function AppModule() {
    }
    return AppModule;
}());
AppModule = __decorate([
    core_1.NgModule({
        // Define the services imported by our app
        imports: [
            platform_browser_1.BrowserModule,
            home_module_1.HomeModule,
            core_module_1.CoreModule.forRoot({ userFirstName: 'John', userLastName: 'Smith' }),
            app_routing_module_1.AppRoutingModule,
            http_1.HttpModule,
            http_1.JsonpModule,
            ng2_toastr_1.ToastModule
        ],
        // Define other components in our module
        declarations: [app_component_1.AppComponent],
        providers: [
            authentication_service_1.AuthService,
            { provide: http_1.XSRFStrategy, useValue: new http_1.CookieXSRFStrategy('csrftoken', 'X-CSRFToken') }
        ],
        // Define the root component
        bootstrap: [app_component_1.AppComponent]
    }),
    __metadata("design:paramtypes", [])
], AppModule);
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map