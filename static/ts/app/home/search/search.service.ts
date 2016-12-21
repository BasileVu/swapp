import {Injectable} from '@angular/core';
import {Headers, Http, Response, URLSearchParams} from '@angular/http';

import { Category } from './category';
import {Item} from "../items/item";
import {Search} from "./search";

@Injectable()
export class SearchService {

    private categoriesUrl = '/api/categories/';  // URL to web API
    private itemsUrl = '/api/items/';

    constructor (private http: Http) {}

    getCategories (): Promise<Category[]> {
        return this.http.get(this.categoriesUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    search (search: Search): Promise<Item[]> {
        let params: URLSearchParams = new URLSearchParams();
        params.set('q', search.q);
        params.set('category', search.category);
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
}
