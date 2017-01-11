import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';
import {User} from "../profile/user";
import {Offer} from "./offer";
import {InventoryItem} from "../inventory/inventory-item";
import {OfferUpdate} from "./offer-update";
import {Note} from "./Note";

@Injectable()
export class OfferService {

    // Observable source
    private openOfferModalSource = new Subject<Array<any>>();
    // Observable boolean streams
    offerModalSelected$ = this.openOfferModalSource.asObservable();

    constructor(private http: Http) { }

    // Service message commands
    // offer is an array where [0]=user, [1]=owner, [2]=item wanted
    openOfferModal(offer: Array<any>) {
        this.openOfferModalSource.next(offer);
    }

    sendOffer(offer: Offer): Promise<any> {
        let body = JSON.stringify(offer); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.post('/api/offers/', body, options)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    // Send whether the offer is accepted or not
    updateOffer(offer_id: number, offerUpdate: OfferUpdate): Promise<any> {
        let body = JSON.stringify(offerUpdate); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.patch('/api/offers/' + offer_id + '/', body, options)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    rateUser(note: Note) {
        let body = JSON.stringify(note); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.post('/api/notes/', body, options)
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

    cloneUser(user: User): User {
        let u = new User();
        u.id = user.id;
        u.profile_picture_url = user.profile_picture_url;
        u.username = user.username;
        u.first_name = user.first_name;
        u.last_name = user.last_name;
        u.location = user.location;
        for (let item of user.items)
            u.items.push(item);
        u.notes = user.notes;
        u.note_avg = user.note_avg;

        return u;
    }
}