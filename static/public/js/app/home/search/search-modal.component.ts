import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';
import {OrderBy} from "./orderby";
import {ItemsService} from "../items/items.service";
import {Search} from "./search";

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
