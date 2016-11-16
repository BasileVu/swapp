import {Component, ViewEncapsulation} from '@angular/core';

import { SearchService } from './search.service';

@Component({
    moduleId: module.id,
    selector: 'search',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './search.component.html'
})
export class SearchComponent {

    // public searchConfiguration:any;
    // private _search:Object;
    //
    // constructor(private _searchService:SearchService) {
    //     this.searchConfiguration = this._searchService.getData();
    //     // this.searchConfiguration.select = (start, end) => this._onSelect(start, end);
    // }
    //
    // public onSearchReady(calendar):void {
    //     this._search = calendar;
    // }
    //
    // private _onSelect(start, end):void {
    //
    //     console.log("search.component.ts _onSelect");
    //     // if (this._calendar != null) {
    //     //     let title = prompt('Event Title:');
    //     //     let eventData;
    //     //     if (title) {
    //     //         eventData = {
    //     //             title: title,
    //     //             start: start,
    //     //             end: end
    //     //         };
    //     //         jQuery(this._calendar).fullCalendar('renderEvent', eventData, true);
    //     //     }
    //     //     jQuery(this._calendar).fullCalendar('unselect');
    //     // }
    // }
}
