import {Injectable} from '@angular/core';
import {Headers, Http, Response} from '@angular/http';

import { Observable }     from 'rxjs/Observable';
import {Item} from "./item";

@Injectable()
export class ItemsService {

    private itemsUrl = '/api/items/';  // URL to web API

    constructor (private http: Http) {}

// TODO : with promise
    getItems (): Promise<Item[]> {
        return this.http.get(this.itemsUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    private extractData(res: Response) {
        let body = res.json();
        return body || { };
    }

    private handleError (error: Response | any) {
        // In a real world app, we might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Promise.reject(errMsg);
    }

    // getItems(): Observable<Item[]> {
    //     return Observ.resolve();
    //     return {
    //         [
    //             {
    //                 id: 1,
    //                 name: "Test",
    //                 description: "Test",
    //                 price_min: 123,
    //                 price_max: 33443,
    //                 creation_date: "2016-11-15T13:17:06.778856Z",
    //                 archived: true,
    //                 owner: 1,
    //                 category: 1
    //             },
    //             {
    //                 id: 2,
    //                 name: "objet 2",
    //                 description: "cdnsajkcl",
    //                 price_min: 21,
    //                 price_max: 34,
    //                 creation_date: "2016-11-15T14:34:26.975681Z",
    //                 archived: false,
    //                 owner: 1,
    //                 category: 1
    //             },
    //             {
    //                 id: 3,
    //                 name: "objet 2",
    //                 description: "cdnsajkcl",
    //                 price_min: 21,
    //                 price_max: 34,
    //                 creation_date: "2016-11-15T14:34:37.781966Z",
    //                 archived: false,
    //                 owner: 1,
    //                 category: 1
    //             }
    //         ]
    //     };
    // }
}
