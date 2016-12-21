// Crazy copy of the app/user.service
// Proves that UserService is an app-wide singleton and only instantiated once
// IFF shared.module follows the `forRoot` pattern
//
// If it didn't, a new instance of UserService would be created
// after each lazy load and the userName would double up.
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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var core_1 = require("@angular/core");
var nextId = 1;
var UserServiceConfig = (function () {
    function UserServiceConfig() {
        this.userFirstName = 'Philip';
        this.userLastName = 'Marlow';
    }
    return UserServiceConfig;
}());
exports.UserServiceConfig = UserServiceConfig;
var UserService = (function () {
    function UserService(config) {
        this.id = nextId++;
        this._userFirstName = 'Sherlock';
        this._userLastName = 'Holmes';
        if (config) {
            this._userFirstName = config.userFirstName;
            this._userLastName = config.userLastName;
        }
    }
    Object.defineProperty(UserService.prototype, "userFirstName", {
        get: function () {
            // Demo: add a suffix if this service has been created more than once
            var suffix = this.id > 1 ? " times " + this.id : '';
            return this._userFirstName + suffix;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(UserService.prototype, "userLastName", {
        get: function () {
            // Demo: add a suffix if this service has been created more than once
            var suffix = this.id > 1 ? " times " + this.id : '';
            return this._userLastName + suffix;
        },
        enumerable: true,
        configurable: true
    });
    return UserService;
}());
UserService = __decorate([
    core_1.Injectable(),
    __param(0, core_1.Optional()),
    __metadata("design:paramtypes", [UserServiceConfig])
], UserService);
exports.UserService = UserService;
/*
 Copyright 2016 Google Inc. All Rights Reserved.
 Use of this source code is governed by an MIT-style license that
 can be found in the LICENSE file at http://angular.io/license
 */ 
//# sourceMappingURL=user.service.js.map