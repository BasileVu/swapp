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
var search_service_1 = require("./search.service");
var category_1 = require("./category");
var orderby_1 = require("./orderby");
var items_service_1 = require("../items/items.service");
var search_1 = require("./search");
var SearchModalComponent = (function () {
    function SearchModalComponent(searchService, itemsService) {
        this.searchService = searchService;
        this.itemsService = itemsService;
        this.errorMessage = "No category available for now";
        this.allCategories = new category_1.Category("All categories");
        this.selectedCategory = new category_1.Category("All categories");
        this.selectedOrderBy = new orderby_1.OrderBy("Recommended", "");
        this.orderBys = [
            new orderby_1.OrderBy("Recommended", ""),
            new orderby_1.OrderBy("Newest", "date"),
            new orderby_1.OrderBy("Name", "name"),
            new orderby_1.OrderBy("Category name", "category"),
            new orderby_1.OrderBy("Cheapest", "price_min"),
            new orderby_1.OrderBy("Most expensive", "price_max"),
            new orderby_1.OrderBy("Closest", "range"),
        ];
        this.hideModal = false;
        this.model = new search_1.Search();
    }
    SearchModalComponent.prototype.ngOnInit = function () {
        this.getCategories();
    };
    SearchModalComponent.prototype.selectCategory = function (category) {
        this.selectedCategory = category;
    };
    SearchModalComponent.prototype.selectOrderBy = function (OrderBy) {
        this.selectedOrderBy = OrderBy;
    };
    SearchModalComponent.prototype.getCategories = function () {
        var _this = this;
        this.searchService.getCategories()
            .then(function (categories) {
            _this.categories = categories;
            _this.categories.unshift(_this.allCategories);
        }, function (error) { return _this.errorMessage = error; });
    };
    SearchModalComponent.prototype.search = function () {
        var _this = this;
        console.log(this.model);
        this.model.category = "";
        if (this.selectedCategory.name != this.allCategories.name) {
            this.model.category = this.selectedCategory.name;
        }
        this.model.orderBy = this.selectedOrderBy;
        this.searchService.search(this.model)
            .then(function (items) { _this.itemsService.updateItems(items); console.log(items); }, function (error) { return _this.errorMessage = error; });
    };
    return SearchModalComponent;
}());
SearchModalComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'search-modal',
        encapsulation: core_1.ViewEncapsulation.None,
        templateUrl: './search-modal.component.html'
    }),
    __metadata("design:paramtypes", [search_service_1.SearchService, items_service_1.ItemsService])
], SearchModalComponent);
exports.SearchModalComponent = SearchModalComponent;
//# sourceMappingURL=search-modal.component.js.map