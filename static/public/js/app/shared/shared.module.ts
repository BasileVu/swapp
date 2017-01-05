import { NgModule }            from '@angular/core';
import { CommonModule }        from '@angular/common';
import { FormsModule }         from '@angular/forms';

import { AuthService }          from './authentication/authentication.service';

@NgModule({
    imports:      [ CommonModule ],
    exports:      [ CommonModule, FormsModule, AuthService ]
})
export class SharedModule { }