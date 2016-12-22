import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';
import { Search } from "./search";
import {ItemsService} from "../items/items.service";

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

    constructor (private searchService: SearchService, private itemsService: ItemsService) {}

    ngOnInit() {
        this.getCategories();
    }

    getCategories() {
        this.searchService.getCategories()
            .then(
                categories => this.categories = categories,
                error =>  this.errorMessage = <any>error);
    }

    search(q, category){
        console.log(q.value);
        this.searchService.search(new Search(q.value, category))
            .then(
                items => { this.itemsService.updateItems(items); console.log(items);},
                error => this.errorMessage = <any>error);
    }
}
