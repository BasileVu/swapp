import {Component, OnInit, ViewEncapsulation} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'profile-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './profile-modal.component.html'
})

export class ProfileModalComponent implements OnInit {

    constructor() {}

    ngOnInit() {
    }
}
