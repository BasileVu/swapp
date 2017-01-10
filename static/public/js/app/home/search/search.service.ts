import {Injectable} from '@angular/core';
import { Http, Response, URLSearchParams} from '@angular/http';
import { Category } from './category';
import {Search} from "./search";
import {DetailedItem} from "../items/detailed-item";
import {BehaviorSubject} from "rxjs/BehaviorSubject";

@Injectable()
export class SearchService {

    private categoriesUrl = '/api/categories/';  // URL to web API
    private itemsUrl = '/api/items/';
    private searchVals: Search = new Search();

    model = new BehaviorSubject<Search>(this.searchVals);

    constructor (private http: Http) {}

    getCategories (): Promise<Category[]> {
        return this.http.get(this.categoriesUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    search (): Promise<DetailedItem[]> {
        let params: URLSearchParams = new URLSearchParams();
        params.set('q', this.model.value.q);
        params.set('category', this.model.value.category.name);
        params.set('order_by', this.model.value.orderBy.value);
        params.set('price_min', this.model.value.price_min);
        params.set('price_max', this.model.value.price_max);
        params.set('range', this.model.value.range);
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
