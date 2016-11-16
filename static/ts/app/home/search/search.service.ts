import {Injectable} from '@angular/core';
import { Headers, Http } from '@angular/http';

@Injectable()
export class SearchService {

    constructor(private http: Http) { }

    getData() {
        return {
            filters: [
                "Recommended",
                "Trends",
                "Latest",
                "Nearest"
            ],
            category: [
                'Animals & Accessories',
                'Art',
                'Audio - TV - Video',
                'Cars',
                'Jewels & Watch',
                'Billets & Voucher',
                'Camping',
                'Movie & DVD',
                'Video Games'
            ]

        };
        // let dashboardColors = this._baConfig.get().colors.dashboard;
        // return {
        //     header: {
        //         left: 'prev,next today',
        //         center: 'title',
        //         right: 'month,agendaWeek,agendaDay'
        //     },
        //     defaultDate: '2016-03-08',
        //     selectable: true,
        //     selectHelper: true,
        //     editable: true,
        //     eventLimit: true,
        //     events: [
        //         {
        //             title: 'All Day Event',
        //             start: '2016-03-01',
        //             color: dashboardColors.silverTree
        //         },
        //         {
        //             title: 'Long Event',
        //             start: '2016-03-07',
        //             end: '2016-03-10',
        //             color: dashboardColors.blueStone
        //         },
        //         {
        //             title: 'Dinner',
        //             start: '2016-03-14T20:00:00',
        //             color: dashboardColors.surfieGreen
        //         },
        //         {
        //             title: 'Birthday Party',
        //             start: '2016-04-01T07:00:00',
        //             color: dashboardColors.gossip
        //         }
        //     ]
        // };
    }
}
