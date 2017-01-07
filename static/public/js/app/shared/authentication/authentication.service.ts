import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

import { User } from '../../home/profile/user';
import { Account } from "../../home/profile/account";

@Injectable()
export class AuthService {

    private loggedIn: boolean;

    // TODO : garder l'utilisateur (username et autres infos) tout le long de sa session
    // Sauver l'utilisateur lors du login et créer des méthodes à disposition des composants
    // pour récupérer cet utilisateur quand nécessaire
    private user: User;

    // Observable source
    private loggedInSelectedSource = new Subject<boolean>();
    private userSelectedSource = new Subject<User>();
    // Observable boolean streams
    loggedInSelected$ = this.loggedInSelectedSource.asObservable();
    userSelected$ = this.userSelectedSource.asObservable();

    constructor(private http: Http) {
        this.loggedIn = false;
    }

    // Service message commands
    selectLoggedIn(loggedIn: boolean) {
        this.loggedInSelectedSource.next(loggedIn);
    }

    selectUser(user: User) {
        this.userSelectedSource.next(user);
    }
    
    isLoggedIn():boolean {
        return this.loggedIn;
    }

    logout(): Promise<any> {
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
            .then(function(response){
                if (response.status === 201) {
                    return response;
                } else {
                    this.handleError(response);
                }
            })
            .catch(this.handleError);
    }

    getAccount(): Promise<Account> {
        return this.http.get('/api/account/')
            .toPromise()
            .then(this.extractUser)
            .catch(this.handleError);
    }

    extractUser(res: Response) {
        let body = res.json();
        let user = new Account();
        user.id = body.id;
        user.profile_picture_url = body.profile_picture_url;
        user.username = body.username;
        user.first_name = body.first_name;
        user.last_name = body.last_name;
        user.email = body.email;
        user.location.street = body.location.street;
        user.location.city = body.location.city;
        user.location.region = body.location.region;
        user.location.country = body.location.country;
        user.last_modification_date = body.last_modification_date;
        user.categories = body.categories;
        user.notes = body.notes;
        user.note_avg = body.note_avg;
        user.items = body.items;
        return user;
    }

    getUser() {
        if (this.loggedIn)
            return this.user;
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

    checkCredentials() {
        //return localStorage.getItem("user") !== null;
        return true;
    }
}