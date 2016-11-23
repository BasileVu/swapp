import {
    Component, ViewEncapsulation, OnInit
} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'inventory',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './inventory.component.html'
})
export class InventoryComponent implements OnInit {

    constructor() { }

    ngOnInit(): void {
    }
}
