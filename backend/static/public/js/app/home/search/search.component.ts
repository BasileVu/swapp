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
    templateUrl: './search.component.html'
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
        this.model = this.searchService.model.value;
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
