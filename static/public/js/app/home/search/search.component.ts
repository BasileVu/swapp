import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';
import { Search } from "./search";
import {ItemsService} from "../items/items.service";
import {OrderBy} from "./OrderBy";

@Component({
    moduleId: module.id,
    selector: 'search',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './search.component.html',
    providers: [SearchService]
})
export class SearchComponent {

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

    constructor (private searchService: SearchService, private itemsService: ItemsService) {}

    ngOnInit() {
        this.getCategories();

        this.searchService.model.subscribe(model => {
            this.model = model;
        });
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
