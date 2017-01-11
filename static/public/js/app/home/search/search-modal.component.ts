import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';
import {OrderBy} from "./orderby";
import {ItemsService} from "../items/items.service";
import {Search} from "./search";
import {AuthService} from "../../shared/authentication/authentication.service";
import {Http, RequestOptions, Headers, Response} from "@angular/http";
import {GoogleService} from "./googleService";

declare let $: any;
declare let google: any;

@Component({
    moduleId: module.id,
    selector: 'search-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './search-modal.component.html'
})
export class SearchModalComponent {

    errorMessage: string = "No category available for now";
    categories: Category[];
    orderBys: OrderBy[] = [
        new OrderBy("Recommended", ""),
        new OrderBy("Newest", "date"),
        new OrderBy("Name", "name"),
        new OrderBy("Category name", "category"),
        new OrderBy("Cheapest", "price_min"),
        new OrderBy("Most expensive", "price_max"),
        new OrderBy("Closest", "range"),
    ];
    model: Search = new Search();
    map: any;
    center: any = {lat: 0, lng: 0};
    advancedSearchModal: any;
    searchLocation: string = '';

    constructor (
        private searchService: SearchService,
        private itemsService: ItemsService,
        private authService: AuthService,
        private googleService: GoogleService
    ) {}

    ngOnInit() {
        let that = this;
        this.getCategories();
        this.model = this.searchService.model.value;
        this.searchService.model.subscribe(newModel => {
            if(typeof that.map !== "undefined") {
                that.setLocation();
            }
        });

        this.authService.getAccount().then(res => {
            this.searchLocation = res.location.street + ', ' +
                                    res.location.city + ', ' +
                                    res.location.country;
        });
        this.advancedSearchModal = $('#advanced-search-modal');
        this.advancedSearchModal.on('show.bs.modal', function (e: any) {
            setTimeout(function () {
                that.map = new google.maps.Map(document.getElementById('search-modal-map'), {
                    scrollwheel: false
                });
                that.setLocation();
            }, 300)
        });
    }

    setLocation() {
        let url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+this.searchLocation+'&key=AIzaSyDNi0DkJRcQiOhJzSitoV5GhlacK6fNtKs';

        this.googleService.find(url).then(
            res => {
                let data: any = this.extractData(res);
                this.center = data.results[0].geometry.location;

                this.recenterMap();
            },
            error => this.handleError(error)
        );

        this.addMarker({lat: -34.197, lng: 150.844});
        this.addMarker({lat: -34.308, lng: 150.679});
        this.addMarker({lat: -34.390, lng: 150.664});
        this.addCircle(10000);
    }

    recenterMap() {
        switch(this.model.range) {
            case'1': {
                this.map.setZoom(9);
                break;
            }
            case'10': {
                this.map.setZoom(8);
                break;
            }
            case'50': {
                this.map.setZoom(7);
                break;
            }
            case'100': {
                this.map.setZoom(6);
                break;
            }
            case'500': {
                this.map.setZoom(5);
                break;
            }
            case'0': {
                this.map.setZoom(2);
                break;
            }
        }
        this.map.setCenter(this.center);
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

    addMarker(positions: any) {
        new google.maps.Marker({
            map: this.map,
            position: positions
        });
    }

    addCircle(radius: number) {
        new google.maps.Circle({
            map: this.map,
            center: this.center,
            radius: radius,    // 10 miles in metres
            fillColor: '#eed5a9',
            fillOpacity: 0.3,
            strokeColor: '#40b2cd',
            strokeOpacity: 1,
            strokeWeight: 3
        });
    }

    ngOnDestroy() {
        this.searchService.model.unsubscribe();
    }

    selectCategory(category: Category) {
        this.model.category = category;
        this.searchService.model.next(this.model);
    }

    selectOrderBy(orderBy: OrderBy) {
        this.model.orderBy = orderBy;
        this.searchService.model.next(this.model);
    }

    newVal(value: any) {
        this.model.q = value;
        this.searchService.model.next(this.model);
    }

    getCategories() {
        this.searchService.getCategories()
            .then(
                 categories => {
                     this.categories = categories;
                     this.categories.unshift(new Category("All categories"));
                 },
                error =>  this.errorMessage = <any>error);
    }

    search(){
        this.searchService.search()
            .then(
                items => { this.itemsService.updateItems(items); },
                error => this.errorMessage = <any>error);
    }
}
