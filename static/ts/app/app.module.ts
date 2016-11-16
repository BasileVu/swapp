import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { HttpModule, JsonpModule } from '@angular/http';

/* App Root */
import { AppComponent }   from './app.component';
import { HomeModule } from './home/home.module';

/* Feature Modules */
// import { ItemsModule }    from './items/items.module';
import { CoreModule }       from './core/core.module';

/* Routing Module */
import { AppRoutingModule } from './app-routing.module';

@NgModule({
    imports: [
        BrowserModule,
        HomeModule,
        /*
         CoreModule,
         */
        CoreModule.forRoot({userFirstName: 'John', userLastName: 'Smith'}),
        AppRoutingModule,
        HttpModule,
        JsonpModule
    ],
    declarations: [ AppComponent ],
    bootstrap:    [ AppComponent ]
})

export class AppModule { }