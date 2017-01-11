import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';
import {OrderBy} from "./orderby";
import {ItemsService} from "../items/items.service";
import {Search} from "./search";
import {AuthService} from "../../shared/authentication/authentication.service";
import {Http, RequestOptions, Headers, Response} from "@angular/http";
import {GoogleService} from "./google.service";
import {DetailedItem} from "../items/detailed-item";
import {Subscription} from "rxjs/Subscription";

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
    markers: any[] = [];
    circle: any;
    center: any = {lat: 0, lng: 0};
    advancedSearchModal: any;
    searchLocation: string = '';
    items: DetailedItem[] = [];
    subscription: Subscription = new Subscription;

    constructor (
        private searchService: SearchService,
        private itemsService: ItemsService,
        private authService: AuthService,
        private googleService: GoogleService
    ) { }

    ngOnInit() {

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                if(loggedIn) {

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
                            that.circle = new google.maps.Circle({
                                map: that.map,
                                center: that.center,
                                radius: 100000,    // 10 miles in metres
                                fillColor: '#eed5a9',
                                fillOpacity: 0.3,
                                strokeColor: '#40b2cd',
                                strokeOpacity: 1,
                                strokeWeight: 3
                            });
                            that.setLocation();
                        }, 300)
                    });

                }
            }
        );

    }

    private setLocation() {
        this.deleteMarkers();
        this.getMarkers();

        let url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+this.searchLocation+'&key=AIzaSyDNi0DkJRcQiOhJzSitoV5GhlacK6fNtKs';

        if (this.searchLocation.length > 3) {
            this.googleService.find(url).then(
                res => {
                    if (typeof res !== "undefined" ) {
                        let data: any = this.extractData(res);

                        if( typeof data.results[0] !== 'undefined') {
                            this.center = data.results[0].geometry.location;
                        this.recenterMap();
                        }
                    }
                },
                error => this.handleError(error)
            );
        }
    }

    private getMarkers() {
        this.search().then(data => {
            for (let item of this.items) {
                this.addMarker({
                    lng: item.owner_coordinates.longitude,
                    lat: item.owner_coordinates.latitude
                });
            }
        });
    }

    private recenterMap() {
        switch(this.model.range) {
            case '1': {
                this.map.setZoom(15);
                break;
            }
            case '10': {
                this.map.setZoom(12);
                break;
            }
            case '50': {
                this.map.setZoom(10);
                break;
            }
            case '100': {
                this.map.setZoom(9);
                break;
            }
            case '500': {
                this.map.setZoom(6);
                break;
            }
            case '0': {
                this.map.setZoom(2);
                break;
            }
        }
        this.changeCircle(parseInt(this.model.range) * 1000);
        this.map.setCenter(this.center);
    }

    private setMapOnAll(map: any) {
        for (let i = 0; i < this.markers.length; i++) {
            this.markers[i].setMap(map);
        }
    }

    private clearMarkers() {
        this.setMapOnAll(null);
    }

    private deleteMarkers() {
        this.clearMarkers();
        this.markers = [];
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
        this.markers.push(new google.maps.Marker({
            map: this.map,
            position: positions
        }));
    }

    private changeCircle(radius: number) {
        this.circle.setRadius(radius/2);
        this.circle.setCenter(this.center);
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

    newLocation(pos: string) {
        this.searchLocation = pos;
        this.setLocation();
    }

    newLowEval(value: string) {
        this.model.price_min = value;
        this.searchService.model.next(this.model);
    }

    newMaxEval(value: string) {
        this.model.price_max = value;
        this.searchService.model.next(this.model);
    }

    selectRange(value: any) {
        this.model.range = value;
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

    search(): Promise<DetailedItem[]> {
        return this.searchService.search()
            .then(
                items => {
                    this.items = items;
                    this.itemsService.updateItems(items);
                },
                error => this.errorMessage = <any>error);
    }
}
