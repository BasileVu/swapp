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
var search_service_1 = require('./search.service');
var SearchComponent = (function () {
    function SearchComponent(searchService) {
        this.searchService = searchService;
        this.errorMessage = "No category available for now";
    }
    SearchComponent.prototype.ngOnInit = function () {
        this.getCategories();
    };
    SearchComponent.prototype.getCategories = function () {
        var _this = this;
        this.searchService.getCategories()
            .then(function (categories) { return _this.categories = categories; }, function (error) { return _this.errorMessage = error; });
    };
    SearchComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'search',
            encapsulation: core_1.ViewEncapsulation.None,
            templateUrl: './search.component.html',
            providers: [search_service_1.SearchService]
        }), 
        __metadata('design:paramtypes', [search_service_1.SearchService])
    ], SearchComponent);
    return SearchComponent;
}());
exports.SearchComponent = SearchComponent;
//# sourceMappingURL=search.component.js.map