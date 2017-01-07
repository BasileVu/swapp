import {Injectable} from '@angular/core';
import {Headers, Http, Response, URLSearchParams} from '@angular/http';

import { Category } from './category';
import {Search} from "./search";
import {DetailedItem} from "../items/detailed-item";

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

    search (s: Search): Promise<DetailedItem[]> {
        let params: URLSearchParams = new URLSearchParams();
        params.set('q', s.q);
        params.set('category', s.category);
        params.set('order_by', s.orderBy.value);
        params.set('price_min', s.price_min);
        params.set('price_max', s.price_max);
        params.set('range', s.range);
        return this.http.get(this.itemsUrl, { search: params })
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
