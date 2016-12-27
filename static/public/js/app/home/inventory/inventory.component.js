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
var authentication_service_1 = require('../../shared/authentication/authentication.service');
var InventoryComponent = (function () {
    function InventoryComponent(authService) {
        this.authService = authService;
    }
    InventoryComponent.prototype.ngOnInit = function () {
        this.loggedIn = this.authService.isLoggedIn();
    };
    InventoryComponent.prototype.ngOnChanges = function () {
        console.log("change loggedIn=" + this.loggedIn);
        // settimeout is an hack to have the inventory displayed nicely.
        // It's probably due to the DOM elements which are not fully loaded
        // on ngOnChanges so we wait a little time (100ms)
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
        }, 100);
    };
    __decorate([
        core_1.Input(), 
        __metadata('design:type', Boolean)
    ], InventoryComponent.prototype, "loggedIn", void 0);
    InventoryComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'inventory',
            encapsulation: core_1.ViewEncapsulation.None,
            templateUrl: './inventory.component.html',
            animations: [
                core_1.trigger('flyInOut', [
                    core_1.state('in', core_1.style({ opacity: 1, transform: 'translateX(0)' })),
                    core_1.transition('void => *', [
                        core_1.style({
                            opacity: 0,
                            transform: 'translateX(0) scale(0)'
                        }),
                        core_1.animate(200)
                    ]),
                    core_1.transition('* => void', [
                        core_1.animate(200, core_1.style({
                            opacity: 0,
                            transform: 'translateX(0) scale(0)'
                        }))
                    ])
                ])
            ]
        }), 
        __metadata('design:paramtypes', [authentication_service_1.AuthService])
    ], InventoryComponent);
    return InventoryComponent;
}());
exports.InventoryComponent = InventoryComponent;
//# sourceMappingURL=inventory.component.js.map