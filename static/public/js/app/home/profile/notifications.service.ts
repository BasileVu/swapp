import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Notification} from "./notification";
import { Observable } from 'rxjs';


@Injectable()
export class NotificationsService {

    private notificationsUrl = 'api/notifications/';

    constructor (private http: Http) {}

    getNotification (): Promise<Notification[]> {
        return this.http.get(this.notificationsUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    private extractData(res: Response) {
        let body = res.json();
        return body || { };
    }

    private handleError (error: Response | any) {
        // TODO : In a real world app, we might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            errMsg = body[0];
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Promise.reject(errMsg);
    }
}