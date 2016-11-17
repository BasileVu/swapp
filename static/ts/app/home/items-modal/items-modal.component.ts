import {Component, ViewEncapsulation, AfterContentInit } from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'items-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items-modal.component.html'
})
export class ItemsModalComponent implements AfterContentInit {

    ngOnInit() {
        console.log('initiated items Modal');
    }

    ngAfterContentInit() {
        console.log("items modal after content init");
    }
}
