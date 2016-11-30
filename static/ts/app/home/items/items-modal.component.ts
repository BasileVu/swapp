import {Component, ViewEncapsulation, OnDestroy, OnInit } from '@angular/core';

import { ItemsService } from './items.service';
import { Item } from "./item";
import { Subscription }   from 'rxjs/Subscription';

@Component({
    moduleId: module.id,
    selector: 'items-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items-modal.component.html'
})
export class ItemsModalComponent implements OnInit, OnDestroy {

    item: Item;
    subscription: Subscription;

    constructor(private itemsService: ItemsService) {
        this.subscription = itemsService.itemSelected$.subscribe(
            item => { this.item = item; }
        );
    }

    ngOnInit() {
    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
