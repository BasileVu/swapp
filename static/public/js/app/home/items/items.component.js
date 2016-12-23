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
var items_service_1 = require("./items.service");
var ItemsComponent = (function () {
    function ItemsComponent(itemsService) {
        this.itemsService = itemsService;
        this.errorMessage = "No items available for now";
    }
    ItemsComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.getItems();
        this.itemsService.getItemsSubject().subscribe(function (items) {
            _this.items = items;
            //grid.arrange();
            // home grid ///////////////////////////
            var grid = $('.grid').isotope({
                // options
                itemSelector: '.grid-item',
                layoutMode: 'masonry'
            });
            // layout only when images are loaded
            grid.imagesLoaded().progress(function () {
                grid.isotope('layout');
            });
            // display items details when hovered
            $('.grid-item').hover(function () {
                $(this).addClass('hovered');
                grid.isotope('layout');
            }, function () {
                $(this).removeClass('hovered');
                grid.isotope('layout');
            });
        });
    };
    ItemsComponent.prototype.getItems = function () {
        var _this = this;
        this.itemsService.getItems()
            .then(function (items) { return _this.items = items; }, function (error) { return _this.errorMessage = error; });
    };
    ItemsComponent.prototype.gotoDetail = function (id) {
        var _this = this;
        console.log("clicked. id: " + id);
        var service = this.itemsService;
        service.getItem(id)
            .then(function (item) {
            _this.selectedItem = item;
            service.selectItem(_this.selectedItem);
        }, function (error) { return _this.errorMessage = error; });
    };
    return ItemsComponent;
}());
ItemsComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'items',
        encapsulation: core_1.ViewEncapsulation.None,
        templateUrl: './items.component.html',
        providers: []
    }),
    __metadata("design:paramtypes", [items_service_1.ItemsService])
], ItemsComponent);
exports.ItemsComponent = ItemsComponent;
//# sourceMappingURL=items.component.js.map