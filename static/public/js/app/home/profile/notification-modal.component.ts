import {Component, ViewEncapsulation, OnInit} from '@angular/core';
import {NotificationsService} from "./notifications.service";
import {Notification} from "./notification";

@Component({
    moduleId: module.id,
    selector: 'notification-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './notification-modal.component.html'
})
export class NotificationModalComponent implements OnInit {

    notifications: Notification[];

    constructor (private notificationsService: NotificationsService) {}

    ngOnInit() {
        this.notificationsService.getNotification().then(res => {
            console.log(res);
        });
    }
}
