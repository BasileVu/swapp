import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Subject }    from 'rxjs/Subject';

@Injectable()
export class ProfileService {

    constructor(private http: Http) { }

    uploadProfilePicture(formData: FormData): Promise<any> {
        return new Promise(function (resolve, reject) {
            let req = new XMLHttpRequest();
            req.open("POST", "/api/images/");
            req.setRequestHeader("enctype", "multipart/form-data");
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
