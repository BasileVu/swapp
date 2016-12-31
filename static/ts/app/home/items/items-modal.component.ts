import {Component, ViewEncapsulation, OnDestroy, OnInit } from '@angular/core';

import { ItemsService } from './items.service';
import { Item } from "./item";
import { Owner } from "./owner";
import { Comment } from "./comment";
import { Subscription }   from 'rxjs/Subscription';

@Component({
    moduleId: module.id,
    selector: 'items-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items-modal.component.html'
})
export class ItemsModalComponent implements OnInit, OnDestroy {

    item: Item;
    owner: Owner;
    comments: Array<Comment>;
    subscription: Subscription;

    constructor(private itemsService: ItemsService) { }

    ngOnInit() {
        this.item = new Item(); // Initiate an empty item. hack to avoid errors
        this.owner = new Owner();
        this.subscription = this.itemsService.itemSelected$.subscribe(
            item => this.item = item
        );
    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
