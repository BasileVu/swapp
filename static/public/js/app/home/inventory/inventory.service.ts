import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';

import { ItemCreationDTO } from './item-creation-dto';
import {ProfileService} from "../profile/profile.service";

@Injectable()
export class InventoryService {

    constructor(private http: Http,
                private profileService: ProfileService) { }

    addItem(itemCreationDTO: ItemCreationDTO): Promise<any> {
        let body = JSON.stringify(itemCreationDTO); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        // No content to return, we just catch errors
        return this.http.post('/api/items/', body, options)
            .toPromise()
            .catch(this.handleError);
    }

    editItem(itemCreationDTO: ItemCreationDTO, item_id: number): Promise<any> {
        let body = JSON.stringify(itemCreationDTO); // Stringify payload
        let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options = new RequestOptions({ headers: headers }); // Create a request option

        // No content to return, we just catch errors
        return this.http.put('/api/items/' + item_id + "/", body, options)
            .toPromise()
            .catch(this.handleError);
    }

    getDeliveryMethods (): Promise<any> {
        return this.http.get('/api/deliverymethods/')
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    // We must add csrftoken in header manually when we user XMLHttpRequest.
    // Without XHR, images can't be upload with enctype multipart/form-data
    addImage(formData: FormData, item_id: number): Promise<any> {

        let csrftoken: string = this.profileService.getCookie("csrftoken");

        return new Promise(function (resolve, reject) {
            let req = new XMLHttpRequest();
            req.open("POST", "/api/items/" + item_id + "/images/");
            req.setRequestHeader("enctype", "multipart/form-data");
            req.setRequestHeader("X-CSRFToken", csrftoken);
            req.send(formData);

            req.onreadystatechange = () => {
                if(req.readyState === 4) {
                    if(req.status === 201) {
                        resolve(req.response);
                    } else {
                        reject(req.response);
                    }
                }
            }
        })
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
