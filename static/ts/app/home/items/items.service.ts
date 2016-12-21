import { Injectable } from '@angular/core';
import {Headers, Http, Response, URLSearchParams} from '@angular/http';
import { Subject }    from 'rxjs/Subject';

import {Item} from "./item";

@Injectable()
export class ItemsService {

    // Observable string sources
    private itemSelectedSource = new Subject<Item>();

    // Observable string streams
    itemSelected$ = this.itemSelectedSource.asObservable();

    private itemsUrl = '/api/items/';  // URL to web API

    constructor (private http: Http) {}

    // Service message commands
    selectItem(item: Item) {
        this.itemSelectedSource.next(item);
    }

    getItems (): Promise<Item[]> {
        return this.http.get(this.itemsUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getItem (id: number): Promise<Item> {
        return this.http.get('/api/items/' + id)
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
}
