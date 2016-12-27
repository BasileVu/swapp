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
var common_1 = require('@angular/common');
var forms_1 = require('@angular/forms');
var home_component_1 = require('./home.component');
var home_routing_1 = require('./home.routing');
var inventory_component_1 = require('./inventory/inventory.component');
var profile_component_1 = require('./profile/profile.component');
var items_component_1 = require('./items/items.component');
var search_component_1 = require('./search/search.component');
var search_modal_component_1 = require('./search/search-modal.component');
var items_modal_component_1 = require('./items/items-modal.component');
var add_item_modal_component_1 = require('./inventory/add-item-modal.component');
var update_profile_modal_component_1 = require('./profile/update-profile-modal.component');
var profile_modal_component_1 = require('./profile/profile-modal.component');
var register_user_modal_component_1 = require('./register/register-user-modal.component');
var send_proposition_modal_component_1 = require('./offers/send-proposition-modal.component');
var accept_proposition_modal_component_1 = require('./offers/accept-proposition-modal.component');
var notification_modal_component_1 = require('./profile/notification-modal.component');
var inventory_service_1 = require('./inventory/inventory.service');
var profile_service_1 = require('./profile/profile.service');
var items_service_1 = require('./items/items.service');
var search_service_1 = require('./search/search.service');
var HomeModule = (function () {
    function HomeModule() {
    }
    HomeModule = __decorate([
        core_1.NgModule({
            imports: [
                common_1.CommonModule,
                forms_1.FormsModule,
                forms_1.ReactiveFormsModule,
                home_routing_1.routing,
            ],
            declarations: [
                inventory_component_1.InventoryComponent,
                profile_component_1.ProfileComponent,
                items_component_1.ItemsComponent,
                search_component_1.SearchComponent,
                search_modal_component_1.SearchModalComponent,
                items_modal_component_1.ItemsModalComponent,
                home_component_1.HomeComponent,
                add_item_modal_component_1.AddItemModalComponent,
                update_profile_modal_component_1.UpdateProfileModalComponent,
                profile_modal_component_1.ProfileModalComponent,
                register_user_modal_component_1.RegisterUserModalComponent,
                notification_modal_component_1.NotificationModalComponent,
                send_proposition_modal_component_1.SendPropositionModalComponent,
                accept_proposition_modal_component_1.AcceptPropositionModalComponent
            ],
            providers: [
                inventory_service_1.InventoryService,
                profile_service_1.ProfileService,
                items_service_1.ItemsService,
                search_service_1.SearchService
            ]
        }), 
        __metadata('design:paramtypes', [])
    ], HomeModule);
    return HomeModule;
}());
exports.HomeModule = HomeModule;
//# sourceMappingURL=home.module.js.map