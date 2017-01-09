import {Component, OnInit, ViewEncapsulation} from '@angular/core';

declare let $: any;

@Component({
    moduleId: module.id,
    selector: 'messages-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: 'messages-modal.component.html'
})

export class MessagesModalComponent implements OnInit {

    constructor() {}

    ngOnInit() {
    }
}
