// Exact copy of app/title.component.ts except import UserService from shared
import { Component, Input } from '@angular/core';
import { UserService }      from '../core/user.service';

@Component({
  moduleId: module.id,
  selector: 'app-title',
  templateUrl: 'title.component.html',
})
export class TitleComponent {

  @Input() subtitle = '';
  title = 'SWAPP';
  user = '';

  constructor(userService: UserService) {
    this.user = userService.userFirstName;
  }

}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/