import {Component, OnInit} from '@angular/core';

import './rxjs-operators';
import {Http} from "@angular/http";

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: 'app.component.html'
})
export class AppComponent implements OnInit {
    subtitle = '(v1)';

    constructor (private http: Http) {}

    ngOnInit() {
        this.http.get("/api/csrf/");
    }
}


/*
 Copyright 2016 Google Inc. All Rights Reserved.
 Use of this source code is governed by an MIT-style license that
 can be found in the LICENSE file at http://angular.io/license
 */