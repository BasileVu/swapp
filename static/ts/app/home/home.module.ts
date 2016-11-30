import { NgModule }      from '@angular/core';
import { CommonModule }  from '@angular/common';
import { FormsModule } from '@angular/forms';

import { HomeComponent } from './home.component';
import { routing }       from './home.routing';

import { InventoryComponent } from './inventory/inventory.component';
import { ProfileComponent } from './profile/profile.component';
import { ItemsComponent } from './items/items.component';
import { SearchComponent } from './search/search.component';
import { SearchModalComponent } from './search-modal/search-modal.component';
import { ItemsModalComponent } from './items/items-modal.component';

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
        HomeComponent
    ],
    providers: [
        InventoryService,
        ProfileService,
        ItemsService,
        SearchService
    ]
})

export class HomeModule {}
