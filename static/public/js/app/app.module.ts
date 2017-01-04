import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { HttpModule, JsonpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';

/* App Root */
import { AppComponent } from './app.component';
import { HomeModule }   from './home/home.module';

/* Feature Modules */
import { CoreModule }  from './core/core.module';
import { AuthService } from './shared/authentication/authentication.service';
import { ToastModule } from 'ng2-toastr/ng2-toastr';

/* Routing Module */
import { AppRoutingModule } from './app-routing.module';

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
        { provide: XSRFStrategy, useValue: new CookieXSRFStrategy('csrftoken', 'X-CSRFToken') }
    ],

    // Define the root component
    bootstrap:    [ AppComponent ]
})

export class AppModule { }