//noinspection ES6UnusedImports
import { NgModule, Component }      from '@angular/core';
import { CommonModule }  from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// External angular2 libraries
import { ImageCropperComponent } from 'ng2-img-cropper';

import { HomeComponent } from './home.component';
import { routing }       from './home.routing';

import { InventoryComponent } from './inventory/inventory.component';
import { ProfileComponent } from './profile/profile.component';
import { ItemsComponent } from './items/items.component';
import { SearchComponent } from './search/search.component';
import { SearchModalComponent } from './search/search-modal.component';
import { ItemsModalComponent } from './items/items-modal.component';
import { AddItemModalComponent } from './inventory/add-item-modal.component';
import { CreateAccountModalComponent } from './profile/create-account-modal.component';
import { UpdateProfileModalComponent } from './profile/update-profile-modal.component';
import { ProfileModalComponent } from './profile/profile-modal.component';
import { RegisterUserModalComponent } from './register/register-user-modal.component';
import { SendPropositionModalComponent } from './offers/send-proposition-modal.component';
import { AcceptPropositionModalComponent } from './offers/accept-proposition-modal.component';
import { NotificationModalComponent } from './profile/notification-modal.component';
import { EditItemModalComponent } from "./inventory/edit-item-modal.component";
import { InfosModalComponent } from "./infos/infos-modal.component";

import { InventoryService } from './inventory/inventory.service';
import { ProfileService } from './profile/profile.service';
import { ItemsService } from './items/items.service';
import { SearchService } from './search/search.service';
import { OfferService } from './offers/offers.service';
import { NotificationsService } from "./profile/notifications.service";

import { MyInventoryDirective } from './offers/my-inventory.directive';
import { YourInventoryDirective } from './offers/your-inventory.directive';
import { UpdateGridDirective } from './items/update-grid.directive';
import { UpdateCarouselDirective } from './items/update-carousel.directive';
import { UpdateInventoryDirective } from './inventory/update-inventory.directive';
import {MessagesModalComponent} from "./messages/messages-modal.component";


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        routing,
    ],
    declarations: [
        InventoryComponent,
        ProfileComponent,
        ItemsComponent,
        SearchComponent,
        SearchModalComponent,
        ItemsModalComponent,
        HomeComponent,
        AddItemModalComponent,
        CreateAccountModalComponent,
        UpdateProfileModalComponent,
        ProfileModalComponent,
        RegisterUserModalComponent,
        NotificationModalComponent,
        SendPropositionModalComponent,
        AcceptPropositionModalComponent,
        ImageCropperComponent,
        MyInventoryDirective,
        YourInventoryDirective,
        UpdateGridDirective,
        UpdateCarouselDirective,
        UpdateInventoryDirective,
        EditItemModalComponent,
        InfosModalComponent,
        MessagesModalComponent
    ],
    providers: [
        InventoryService,
        ProfileService,
        ItemsService,
        SearchService,
        OfferService,
        NotificationsService
    ]
})

export class HomeModule {}
