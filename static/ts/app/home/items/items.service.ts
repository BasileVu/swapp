import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

import {Item} from "./item";
import {Owner} from "./owner";
import {Comment} from "./comment";
import {Observable} from "rxjs";

@Injectable()
export class ItemsService {

    // Observable string sources
    private itemSelectedSource = new Subject<Item>();
    private ownerSelectedSource = new Subject<Owner>();
    private commentsSelectedSource = new Subject<Comment[]>();

    // Observable string streams
    itemSelected$ = this.itemSelectedSource.asObservable();
    ownerSelected$ = this.ownerSelectedSource.asObservable();
    commentsSelected$ = this.commentsSelectedSource.asObservable();

    private itemsSubject: Subject<Item[]> = new Subject<Item[]>();

    private itemsUrl = '/api/items/';  // URL to web API

    constructor (private http: Http) {}

    // Service message commands
    selectItem(item: Item) {
        this.itemSelectedSource.next(item);
    }

    selectOwner(owner: Owner) {
        this.ownerSelectedSource.next(owner);
    }

    selectComments(comments: Comment[]) {
        this.commentsSelectedSource.next(comments);
    }

    updateItems(items: Item[]){
        this.itemsSubject.next(items);
    }

    getItemsSubject(): Observable<Item[]> {
        return this.itemsSubject.asObservable();
    }

    getItems (): Promise<Item[]> {
        return this.http.get(this.itemsUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getItem (id: number): Promise<Item> {
        return this.http.get(this.itemsUrl + id)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getOwner (owner_id: number): Promise<Owner> {
        return this.http.get('/api/users/' + owner_id)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getComments (item_id: number): Promise<Comment[]> {
        return this.http.get(this.itemsUrl + item_id + '/comments')
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
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Promise.reject(errMsg);
    }
}
