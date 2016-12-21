import {Component, ViewEncapsulation, OnInit} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'accept-proposition-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './accept-proposition-modal.component.html'
})
export class AcceptPropositionModalComponent implements OnInit {
    constructor () {}

    ngOnInit() {
    }
}
