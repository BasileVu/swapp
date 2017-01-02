import {Component, ViewEncapsulation, OnInit} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'notification-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './notification-modal.component.html'
})

export class NotificationModalComponent implements OnInit {

    constructor() {}

    ngOnInit() {
    }
}
