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
var items_service_1 = require('./items.service');
var item_1 = require("./item");
var ItemsModalComponent = (function () {
    function ItemsModalComponent(itemsService) {
        this.itemsService = itemsService;
    }
    ItemsModalComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.item = new item_1.Item(); // Initiate an empty item. hack to avoid errors
        this.subscription = this.itemsService.itemSelected$.subscribe(function (item) { return _this.item = item; });
    };
    ItemsModalComponent.prototype.ngOnDestroy = function () {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    };
    ItemsModalComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'items-modal',
            encapsulation: core_1.ViewEncapsulation.None,
            templateUrl: './items-modal.component.html'
        }), 
        __metadata('design:paramtypes', [items_service_1.ItemsService])
    ], ItemsModalComponent);
    return ItemsModalComponent;
}());
exports.ItemsModalComponent = ItemsModalComponent;
//# sourceMappingURL=items-modal.component.js.map