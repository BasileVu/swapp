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
/* tslint:disable */
// Exact copy of contact/highlight.directive except for color and message
var core_1 = require('@angular/core');
var HighlightDirective = (function () {
    function HighlightDirective(renderer, el) {
        renderer.setElementStyle(el.nativeElement, 'backgroundColor', 'white');
        console.log("* Shared highlight called for " + el.nativeElement.tagName);
    }
    HighlightDirective = __decorate([
        core_1.Directive({ selector: '[highlight], input' }), 
        __metadata('design:paramtypes', [core_1.Renderer, core_1.ElementRef])
    ], HighlightDirective);
    return HighlightDirective;
}());
exports.HighlightDirective = HighlightDirective;
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/ 
//# sourceMappingURL=highlight.directive.js.map