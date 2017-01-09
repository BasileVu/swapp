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
    allCategories: Category = new Category("All categories");
    selectedCategory: Category = new Category("All categories");
    selectedOrderBy = new OrderBy("Recommended", "");
    orderBys: OrderBy[] = [
        new OrderBy("Recommended", ""),
        new OrderBy("Newest", "date"),
        new OrderBy("Name", "name"),
        new OrderBy("Category name", "category"),
        new OrderBy("Cheapest", "price_min"),
        new OrderBy("Most expensive", "price_max"),
        new OrderBy("Closest", "range"),
    ];
    hideModal: boolean = false;
    model: Search = new Search();

    constructor (private searchService: SearchService, private itemsService: ItemsService) {}

    ngOnInit() {
        this.getCategories();
        this.model.range = '100';

        let advancedSearchModal = $('#advanced-search-modal');
        advancedSearchModal.on('show.bs.modal', function (e: any) {
            setTimeout(function () {
                let map = new google.maps.Map(document.getElementById('search-modal-map'), {
                    center: {lat: -34.397, lng: 150.644},
                    scrollwheel: false,
                    zoom: 8
                });
                new google.maps.Marker({
                    map: map,
                    position: {lat: -34.197, lng: 150.844}
                });
                new google.maps.Marker({
                    map: map,
                    position: {lat: -34.308, lng: 150.679},
                });
                new google.maps.Marker({
                    map: map,
                    position: {lat: -34.390, lng: 150.664}
                });
                new google.maps.Circle({
                    map: map,
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

    selectCategory(category: Category){
        this.selectedCategory = category;
    }

    selectOrderBy(OrderBy: OrderBy){
        this.selectedOrderBy = OrderBy;
    }

    getCategories() {
        this.searchService.getCategories()
            .then(
                 categories => {
                     this.categories = categories;
                     this.categories.unshift(this.allCategories);
                 },
                error =>  this.errorMessage = <any>error);
    }

    search(){
        console.log(this.model);
        this.model.category = "";
        if(this.selectedCategory.name != this.allCategories.name){
            this.model.category = this.selectedCategory.name;
        }
        this.model.orderBy = this.selectedOrderBy;
        this.searchService.search(this.model)
            .then(
                items => { this.itemsService.updateItems(items); },
                error => this.errorMessage = <any>error);
    }
}
