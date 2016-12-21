import {Component, ViewEncapsulation, OnInit} from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'register-user-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './register-user-modal.component.html'
})
export class RegisterUserModalComponent implements OnInit {

    constructor () {}

    ngOnInit() {
    }
}
