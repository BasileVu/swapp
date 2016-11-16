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
// Exact copy of app/title.component.ts except import UserService from shared
var core_1 = require('@angular/core');
var user_service_1 = require('../core/user.service');
var TitleComponent = (function () {
    function TitleComponent(userService) {
        this.subtitle = '';
        this.title = 'Swapp';
        this.user = '';
        this.user = userService.userFirstName;
    }
    __decorate([
        core_1.Input(), 
        __metadata('design:type', Object)
    ], TitleComponent.prototype, "subtitle", void 0);
    TitleComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'app-title',
            templateUrl: 'title.component.html',
        }), 
        __metadata('design:paramtypes', [user_service_1.UserService])
    ], TitleComponent);
    return TitleComponent;
}());
exports.TitleComponent = TitleComponent;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=title.component.js.map