import {Injectable} from '@angular/core';
import { Headers, Http } from '@angular/http';

@Injectable()
export class InventoryService {

    constructor(private http: Http) { }

    getData() {
        return {
            items: [
                {
                    title: 'Guitar',
                    image: 'http://placehold.it/400x400'
                },
                {
                    title: 'Guitar',
                    image: 'http://placehold.it/400x400'
                },
                {
                    title: 'Guitar',
                    image: 'http://placehold.it/400x400'
                },
                {
                    title: 'Guitar',
                    image: 'http://placehold.it/400x400'
                },
                {
                    title: 'Guitar',
                    image: 'http://placehold.it/400x400'
                },
                {
                    title: 'Guitar',
                    image: 'http://placehold.it/400x400'
                },
            ]

        };
    }
}
