import {Injectable} from '@angular/core';
import { Headers, Http } from '@angular/http';

@Injectable()
export class SearchService {

    constructor(private http: Http) { }

    getData() {
        return {
            filters: [
                "Recommended",
                "Trends",
                "Latest",
                "Nearest"
            ],
            category: [
                'Animals & Accessories',
                'Art',
                'Audio - TV - Video',
                'Cars',
                'Jewels & Watch',
                'Billets & Voucher',
                'Camping',
                'Movie & DVD',
                'Video Games'
            ]

        };
    }
}
