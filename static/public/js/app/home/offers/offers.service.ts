import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

@Injectable()
export class OfferService {

    // Observable source
    private openOfferModalSource = new Subject<boolean>();
    // Observable boolean streams
    offerModalSelected$ = this.openOfferModalSource.asObservable();

    constructor(private http: Http) { }

    // Service message commands
    // offer is an array where [0]=user, [1]=owner, [2]=item wanted
    openOfferModal(offer) {
        this.openOfferModalSource.next(offer);
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
            .then(function(response){
                if (response.status === 201) {
                    return response;
                } else {
                    this.handleError(response);
                }
            })
            .catch(this.handleError);
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