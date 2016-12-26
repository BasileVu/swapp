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
/* tslint:disable:member-ordering no-unused-variable */
var core_1 = require('@angular/core');
var common_1 = require('@angular/common');
var title_component_1 = require('./title.component');
var user_service_1 = require('./user.service');
var user_service_2 = require('./user.service');
var CoreModule = (function () {
    function CoreModule(parentModule) {
        if (parentModule) {
            throw new Error('CoreModule is already loaded. Import it in the AppModule only');
        }
    }
    CoreModule.forRoot = function (config) {
        return {
            ngModule: CoreModule,
            providers: [
                { provide: user_service_2.UserServiceConfig, useValue: config }
            ]
        };
    };
    CoreModule = __decorate([
        core_1.NgModule({
            imports: [common_1.CommonModule],
            declarations: [title_component_1.TitleComponent],
            exports: [title_component_1.TitleComponent],
            providers: [user_service_1.UserService]
        }),
        __param(0, core_1.Optional()),
        __param(0, core_1.SkipSelf()), 
        __metadata('design:paramtypes', [CoreModule])
    ], CoreModule);
    return CoreModule;
}());
exports.CoreModule = CoreModule;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=core.module.js.map