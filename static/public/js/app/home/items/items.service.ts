import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';
import { Observable } from 'rxjs';

import { Item } from './item';
import { DetailedItem } from './detailed-item';
import { Owner } from './owner';
import { Comment } from './comment';
import { CommentCreationDTO } from './comment-creation-dto';

@Injectable()
export class ItemsService {

    // Observable string sources
    private itemSelectedSource = new Subject<DetailedItem>();
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
    selectItem(item: DetailedItem) {
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

    getDetailedItem (id: number): Promise<DetailedItem> {
        return this.http.get(this.itemsUrl + id)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getOwner (owner_username: string): Promise<Owner> {
        return this.http.get('/api/users/' + owner_username)
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

    addComment (commentCreationDTO: CommentCreationDTO): Promise<any> {
        let body = JSON.stringify(commentCreationDTO); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.post('/api/comments/', body, options)
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