import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

import { User } from '../../home/profile/user';

@Injectable()
export class AuthService {

    private loggedIn: boolean;

    // TODO : garder l'utilisateur (username et autres infos) tout le long de sa session
    // Sauver l'utilisateur lors du login et créer des méthodes à disposition des composants
    // pour récupérer cet utilisateur quand nécessaire
    private user: User;

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

    logout(): Promise<any> {
        localStorage.removeItem("user");
        return this.http.get('/api/logout/')
        .toPromise()
        .catch(this.handleError);
    }
    
    login(userLoginDTO): Promise<any> {
        let body = JSON.stringify(userLoginDTO); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        // No content to return, we just catch errors
        return this.http.post('/api/login/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

    register(userCreationDTO): Promise<any> {
        let body = JSON.stringify(userCreationDTO); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        // No content to return, we just catch errors
        return this.http.post('/api/users/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

    getAccount(): Promise<User> {
        return this.http.get('/api/account/')
            .toPromise()
            .then(this.extractUser)
            .catch(this.handleError);
    }

    extractUser(res: Response) {
        let body = res.json();
        return new User(
                    body.username, // TODO : change with body.profile_picture_url when available on endpoint
                    body.username,
                    body.first_name,
                    body.last_name,
                    body.email,
                    body.location.street,
                    body.location.city,
                    body.location.region,
                    body.location.country,
                    body.location.last_modification_date,
                    body.notes,
                    body.likes,
                    body.items);
    }

    getUser() {
        return this.user;
    }

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