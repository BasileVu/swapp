import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

import { User } from '../../home/profile/user';

@Injectable()
export class AuthService {

    private loggedIn: boolean;

    // Observable source
    private loggedInSelectedSource = new Subject<boolean>();
    // Observable boolean streams
    loggedInSelected$ = this.loggedInSelectedSource.asObservable();

    constructor(private http: Http) {
        this.loggedIn = false;
    }

    // Service message commands
    selectLoggedIn(loggedIn: boolean) {
        this.loggedInSelectedSource.next(loggedIn);
    }
    
    isLoggedIn():boolean {
        return this.loggedIn;
    }

    logout() {
        localStorage.removeItem("user");
    }
    
    login(username, password): Promise<any> {
        let body = JSON.stringify({ username:username, password:password }); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        // No content to return, we just catch errors
        return this.http.post('/api/login/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

/*
    private extractData(res: Response) {
        console.log("Response: " + res);
        let body = res.json();
        return body || { };
    }
*/
    private handleError (error: Response | any) {
        // TODO : In a real world app, we might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error("error: " + errMsg);
        return Promise.reject(errMsg);
    }

    checkCredentials() {
        //return localStorage.getItem("user") !== null;
        return true;
    }
}