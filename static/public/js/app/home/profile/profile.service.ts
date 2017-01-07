import { Injectable } from '@angular/core';
import {Response, Headers, RequestOptions, Http} from '@angular/http';

@Injectable()
export class ProfileService {

    constructor(private http: Http) {
    }

    // We must add csrftoken in header manually when we user XMLHttpRequest.
    // Without XHR, images can't be upload with enctype multipart/form-data
    addImage(formData: FormData): Promise<any> {
        
        let csrftoken: string = this.getCookie("csrftoken");

        return new Promise(function (resolve, reject) {
            let req = new XMLHttpRequest();
            req.open("POST", "/api/images/");
            req.setRequestHeader("enctype", "multipart/form-data");
            req.setRequestHeader("X-CSRFToken", csrftoken);
            req.send(formData);

            req.onreadystatechange = () => {
                if(req.readyState === 4) {
                    if(req.status === 201) {
                        resolve(req.response);
                    } else {
                        reject(req.response);
                    }
                }
            }
        })
        .catch(this.handleError);
    }

    // Get cookie value from its name
    getCookie(name: string): string {
        let value = "; " + document.cookie;
        let parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    updateLocation(location: any): Promise<any> {
        let body = JSON.stringify(location); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.put('/api/account/location/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

    updateCategories(categories: Array<number>): Promise<any> {
        let body = JSON.stringify(categories); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.put('/api/account/categories/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

    updatePassword(password: any): Promise<any> {
        let body = JSON.stringify(password); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.put('/api/account/password/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

    updateAccount(account: any): Promise<any> {
        let body = JSON.stringify(account); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.patch('/api/account/password/', body, options)
            .toPromise()
            .catch(this.handleError);
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
