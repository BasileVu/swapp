import {Component, ViewEncapsulation, OnInit, Input} from '@angular/core';
import {NotificationsService} from "./notifications.service";
import {Notification} from "./notification";
import {Subscription} from "rxjs";
import {AuthService} from "../../shared/authentication/authentication.service";

@Component({
    moduleId: module.id,
    selector: 'notification-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './notification-modal.component.html'
})
export class NotificationModalComponent implements OnInit {

    notifications: Notification[];
    @Input() loggedIn: boolean ;
    subscription: Subscription;

    constructor (private notificationsService: NotificationsService, private authService: AuthService) {}

    ngOnInit() {
        this.loggedIn = this.authService.isLoggedIn();
    }

    ngOnChanges() {
        console.log(this.loggedIn);
        if (this.loggedIn) {
            this.notificationsService.getNotification().then(res => {
                console.log(res);
            });
        }
    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
