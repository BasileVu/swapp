import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {AuthService} from "../../shared/authentication/authentication.service";
import {Subscription} from "rxjs";

declare let $: any;
declare let google: any;

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
