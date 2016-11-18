import {Component, ViewEncapsulation, OnInit, AfterViewInit } from '@angular/core';
import {Observable} from 'rxjs';

@Component({
    moduleId: module.id,
    selector: 'home',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './home.component.html'
})

export class HomeComponent implements OnInit, AfterViewInit {

    constructor(){}

    ngOnInit() {}

    ngAfterViewInit() {
    }

}
