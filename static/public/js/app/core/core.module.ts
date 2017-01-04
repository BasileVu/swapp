/* tslint:disable:member-ordering no-unused-variable */
import {
    NgModule,
    Optional, SkipSelf, ModuleWithProviders
}       from '@angular/core';

import { CommonModule }      from '@angular/common';

import { TitleComponent }    from './title.component';

@NgModule({
    imports:      [ CommonModule ],
    declarations: [ TitleComponent ],
    exports:      [ TitleComponent ]
})
export class CoreModule {

    constructor (@Optional() @SkipSelf() parentModule: CoreModule) {
        if (parentModule) {
            throw new Error(
                'CoreModule is already loaded. Import it in the AppModule only');
        }
    }

    static forRoot(): ModuleWithProviders {
        return {
            ngModule: CoreModule
        };
    }
}