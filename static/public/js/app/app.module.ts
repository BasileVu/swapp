import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import {
    HttpModule, JsonpModule, CookieXSRFStrategy,
    XSRFStrategy, Request
} from '@angular/http';

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
import {GoogleService} from "./home/search/google.service";

export class MyXSRFStrategy {
    configureRequest(req: Request) {
        if (req.url.substr(0,4) === "/api") {
            req.headers.append('X-CSRFToken', this.getCookie('csrftoken'));
        } else {
            req.headers.delete('X-CSRFToken');
        }
    }

    // Get cookie value from its name
    getCookie(name: string): string {
        let value = "; " + document.cookie;
        let parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }
}

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
        GoogleService,
        { provide: XSRFStrategy, useFactory: () => new MyXSRFStrategy() }
    ],

    // Define the root component
    bootstrap:    [ AppComponent ]
})

export class AppModule {}