import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';
import { Category } from './category';

@Component({
    moduleId: module.id,
    selector: 'search-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './search-modal.component.html'
})
export class SearchModalComponent {

    errorMessage: string = "No category available for now";
    categories: Category[];

    constructor (private searchService: SearchService) {}

    ngOnInit() {
        this.getCategories();
    }

    getCategories() {
        this.searchService.getCategories()
            .then(
                categories => this.categories = categories,
                error =>  this.errorMessage = <any>error);
    }
}
