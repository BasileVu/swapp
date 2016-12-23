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
var search_1 = require("./search");
var items_service_1 = require("../items/items.service");
var OrderBy_1 = require("./OrderBy");
var SearchComponent = (function () {
    function SearchComponent(searchService, itemsService) {
        this.searchService = searchService;
        this.itemsService = itemsService;
        this.errorMessage = "No category available for now";
        this.allCategories = new category_1.Category("All categories");
        this.selectedCategory = new category_1.Category("All categories");
        this.selectedOrderBy = new OrderBy_1.OrderBy("Recommended", "");
        this.orderBys = [
            new OrderBy_1.OrderBy("Recommended", ""),
            new OrderBy_1.OrderBy("Newest", "date"),
            new OrderBy_1.OrderBy("Name", "name"),
            new OrderBy_1.OrderBy("Category name", "category"),
            new OrderBy_1.OrderBy("Cheapest", "price_min"),
            new OrderBy_1.OrderBy("Most expensive", "price_max"),
            new OrderBy_1.OrderBy("Closest", "range"),
        ];
    }
    SearchComponent.prototype.ngOnInit = function () {
        this.getCategories();
    };
    SearchComponent.prototype.selectCategory = function (category) {
        this.selectedCategory = category;
    };
    SearchComponent.prototype.selectOrderBy = function (OrderBy) {
        this.selectedOrderBy = OrderBy;
    };
    SearchComponent.prototype.getCategories = function () {
        var _this = this;
        this.searchService.getCategories()
            .then(function (categories) {
            _this.categories = categories;
            _this.categories.unshift(_this.allCategories);
        }, function (error) { return _this.errorMessage = error; });
    };
    SearchComponent.prototype.search = function (q) {
        var _this = this;
        console.log(q.value);
        var category = "";
        if (this.selectedCategory.name != this.allCategories.name) {
            category = this.selectedCategory.name;
        }
        this.searchService.search(new search_1.Search(q.value, category, this.selectedOrderBy.value))
            .then(function (items) { _this.itemsService.updateItems(items); console.log(items); }, function (error) { return _this.errorMessage = error; });
    };
    return SearchComponent;
}());
SearchComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'search',
        encapsulation: core_1.ViewEncapsulation.None,
        templateUrl: './search.component.html',
        providers: [search_service_1.SearchService]
    }),
    __metadata("design:paramtypes", [search_service_1.SearchService, items_service_1.ItemsService])
], SearchComponent);
exports.SearchComponent = SearchComponent;
//# sourceMappingURL=search.component.js.map