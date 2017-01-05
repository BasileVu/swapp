import {
    Component, 
    Input, 
    ViewEncapsulation, 
    OnInit,
    trigger,
    state,
    style,
    transition,
    animate,
} from '@angular/core';

import { AuthService } from '../../shared/authentication/authentication.service';
import { InventoryItem } from './inventory-item';
import { ItemsService } from '../items/items.service';
import {Subscription} from "rxjs";
import {User} from "../profile/user";

declare var $:any;

@Component({
    moduleId: module.id,
    selector: 'inventory',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './inventory.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({opacity: 1, transform: 'translateX(0)'})),
            transition('void => *', [
                style({
                    opacity: 0,
                    transform: 'translateX(0) scale(0)'
                }),
                animate(200)
            ]),
            transition('* => void', [
                animate(200, style({
                    opacity: 0,
                    transform: 'translateX(0) scale(0)'
                }))
            ])
        ])
    ]
})
export class InventoryComponent implements OnInit {

    @Input() loggedIn: boolean;

    owner: User;
    subscription: Subscription;

    private inventory: Array<InventoryItem> = [];
    
    constructor(private authService: AuthService,
                private itemsService: ItemsService) {}

    ngOnInit(): void {
        this.loggedIn = this.authService.isLoggedIn();

        // Listen for user login. We know that when user is available it means
        // that he successfully logged in
        this.subscription = this.authService.userSelected$.subscribe(
            user => {
                this.owner = user;
                for(let item of this.owner.items) {
                    let inventoryItem = new InventoryItem(item.id, item.name, item.image_url, null);
                    console.log(inventoryItem);
                    this.inventory.push(inventoryItem);
                }
            }
        );
    }

    // We receive an ItemCreationDTO object so we'll change it into an InventoryItem
    addItemEvent($event) {
        let inventoryItem = new InventoryItem(
            $event.url,
            $event.name, 
            $event.images[0], 
            $event.creation_date);
        
        this.inventory.push(inventoryItem);

        console.log("inventory:");
        console.log(this.inventory);
    }

    gotoDetail(item_id: number): void {
        console.log("clicked. item_id: " + item_id);

        let service = this.itemsService;
        service.getDetailedItem(item_id)
            .then(
                item => {
                    service.selectItem(item);
                },
                error => console.log(error));

        /*
        service.getOwner(owner_id)
            .then(
                owner => {
                    service.selectOwner(owner);
                },
                error => console.log(error));
                */

        service.getComments(item_id)
            .then(
                comments => {
                    service.selectComments(comments);
                },
                error => console.log(error));
    }
}
