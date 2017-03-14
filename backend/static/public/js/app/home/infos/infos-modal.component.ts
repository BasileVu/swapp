import {Component, OnInit, ViewEncapsulation} from '@angular/core';

declare let $: any;

@Component({
    moduleId: module.id,
    selector: 'infos-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './infos-modal.component.html'
})

export class InfosModalComponent implements OnInit {

    constructor() {}

    ngOnInit() {
    }
}
