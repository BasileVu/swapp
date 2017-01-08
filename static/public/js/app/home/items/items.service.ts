import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';
import { Observable } from 'rxjs';

import { DetailedItem } from './detailed-item';
import { Comment } from './comment';
import { CommentCreationDTO } from './comment-creation-dto';
import {User} from "../profile/user";
import {Like} from "./like";
import {ProfileService} from "../profile/profile.service";
import {InventoryItem} from "../inventory/inventory-item";

@Injectable()
export class ItemsService {

    // Observable string sources
    private itemSelectedSource = new Subject<DetailedItem>();
    private userSelectedSource = new Subject<User>();
    private commentsSelectedSource = new Subject<Comment[]>();

    // Observable string streams
    itemSelected$ = this.itemSelectedSource.asObservable();

    private itemsSubject: Subject<DetailedItem[]> = new Subject<DetailedItem[]>();

    private itemsUrl = '/api/items/';  // URL to web API

    constructor (private http: Http) {}

    // Service message commands
    selectItem(item: DetailedItem) {
        this.itemSelectedSource.next(item);
    }

    selectUser(user: User) {
        this.userSelectedSource.next(user);
    }

    selectComments(comments: Comment[]) {
        this.commentsSelectedSource.next(comments);
    }

    updateItems(items: DetailedItem[]){
        this.itemsSubject.next(items);
    }

    getItemsSubject(): Observable<DetailedItem[]> {
        return this.itemsSubject.asObservable();
    }

    getItems (): Promise<DetailedItem[]> {
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

    getUser (owner_username: string): Promise<User> {
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

    like(l: Like): Promise<any> {
        let body = JSON.stringify(l); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        return this.http.post('/api/likes/', body, options)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    archiveItem(item: number) {
        return this.http.post(this.itemsUrl + item + "/archive/", null)
            .toPromise()
            .catch(this.handleError);
    }

    restoreItem(item: number) {
        return this.http.post(this.itemsUrl + item + "/restore/", null)
            .toPromise()
            .catch(this.handleError);
    }

    private extractData(res: Response) {
        let body = res.json();
        return body || { };
    }

    private handleError (error: Response | any) {
        console.log(error);
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
