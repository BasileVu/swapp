import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

import { ItemCreationDTO } from './item-creation-dto';

@Injectable()
export class InventoryService {

    constructor(private http: Http) { }

    addItem(itemCreationDTO: ItemCreationDTO): Promise<any> {
        let body = JSON.stringify(itemCreationDTO); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        // No content to return, we just catch errors
        return this.http.post('/api/items/', body, options)
            .toPromise()
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
}
