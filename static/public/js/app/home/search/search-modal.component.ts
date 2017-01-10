import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';
import {OrderBy} from "./orderby";
import {ItemsService} from "../items/items.service";
import {Search} from "./search";

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
    advancedSearchModal: any;

    constructor (private searchService: SearchService, private itemsService: ItemsService) {}

    ngOnInit() {
        this.getCategories();
        this.model = this.searchService.model.value;

        this.advancedSearchModal = $('#advanced-search-modal');
        this.advancedSearchModal.on('show.bs.modal', function (e: any) {
            setTimeout(function () {
                this.map = new google.maps.Map(document.getElementById('search-modal-map'), {
                    center: {lat: -34.397, lng: 150.644},
                    scrollwheel: false,
                    zoom: 8
                });
                new google.maps.Marker({
                    map: this.map,
                    position: {lat: -34.197, lng: 150.844}
                });
                new google.maps.Marker({
                    map: this.map,
                    position: {lat: -34.308, lng: 150.679},
                });
                new google.maps.Marker({
                    map: this.map,
                    position: {lat: -34.390, lng: 150.664}
                });
                new google.maps.Circle({
                    map: this.map,
                    center: {lat: -34.397, lng: 150.644},
                    radius: 100000,    // 10 miles in metres
                    fillColor: '#eed5a9',
                    fillOpacity: 0.3,
                    strokeColor: '#40b2cd',
                    strokeOpacity: 1,
                    strokeWeight: 3
                });
            }, 300)
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
