import {
    Component, ViewEncapsulation, OnInit, Input,
    EventEmitter, Output
} from '@angular/core';
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

    @Input() loggedIn: boolean;
    @Output() notificationEvent = new EventEmitter();

    notifications: Notification[];
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
                this.notifications = res;
                this.notificationEvent.emit(this.notifications.length);
            });
        }
    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
