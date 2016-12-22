import { NgModule }      from '@angular/core';
import { CommonModule }  from '@angular/common';
import { FormsModule } from '@angular/forms';

import { HomeComponent } from './home.component';
import { routing }       from './home.routing';

import { InventoryComponent } from './inventory/inventory.component';
import { ProfileComponent } from './profile/profile.component';
import { ItemsComponent } from './items/items.component';
import { SearchComponent } from './search/search.component';
import { SearchModalComponent } from './search/search-modal.component';
import { ItemsModalComponent } from './items/items-modal.component';
import { AddItemModalComponent } from './inventory/add-item-modal.component';
import { UpdateProfileModalComponent } from './profile/update-profile-modal.component';
import { ProfileModalComponent } from './profile/profile-modal.component';
import { RegisterUserModalComponent } from './register/register-user-modal.component';
import { SendPropositionModalComponent } from './offers/send-proposition-modal.component';
import { AcceptPropositionModalComponent } from './offers/accept-proposition-modal.component';
import { NotificationModalComponent } from './profile/notification-modal.component';

import { InventoryService } from './inventory/inventory.service';
import { ProfileService } from './profile/profile.service';
import { ItemsService } from './items/items.service';
import { SearchService } from './search/search.service';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
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
        UpdateProfileModalComponent,
        ProfileModalComponent,
        RegisterUserModalComponent,
        NotificationModalComponent,
        SendPropositionModalComponent,
        AcceptPropositionModalComponent
    ],
    providers: [
        InventoryService,
        ProfileService,
        ItemsService,
        SearchService
    ]
})

export class HomeModule {}
