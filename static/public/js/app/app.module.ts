import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { HttpModule, JsonpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';

/* App Root */
import { AppComponent } from './app.component';
import { HomeModule }   from './home/home.module';

/* Feature Modules */
import { CoreModule }  from './core/core.module';
import { ToastModule } from 'ng2-toastr/ng2-toastr';

/* My modules */
import { AuthService } from './shared/authentication/authentication.service';

/* Routing Module */
import { AppRoutingModule } from './app-routing.module';
import {GoogleService} from "./home/search/googleService";

// Declare the NgModule decorator
@NgModule({

    // Define the services imported by our app
    imports: [
        BrowserModule,
        HomeModule,
        CoreModule,
        AppRoutingModule,
        HttpModule,
        JsonpModule,
        ToastModule
    ],
    
    // Define other components in our module
    declarations: [ AppComponent ],
    
    providers: [ 
        AuthService,
        GoogleService
    ],

    // Define the root component
    bootstrap:    [ AppComponent ]
})

export class AppModule { }