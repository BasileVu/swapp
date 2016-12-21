import {
    Component, ViewEncapsulation, OnInit
} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'add-item-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './add-item-modal.component.html'
})
export class AddItemModalComponent implements OnInit {

    constructor() { }

    ngOnInit(): void {
    }
}
