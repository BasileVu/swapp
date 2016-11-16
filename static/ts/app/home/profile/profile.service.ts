import {Injectable} from '@angular/core';
import { Headers, Http } from '@angular/http';

@Injectable()
export class ProfileService {

    constructor(private http: Http) { }

    getData() {
        return {
            id: 1,
            firstName: 'Mark',
            lastName: 'Wiggel',
            address: 'Rue de la Plaine 40, Yverdon'
        };
    }
}
