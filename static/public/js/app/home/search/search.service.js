"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var http_1 = require('@angular/http');
var SearchService = (function () {
    function SearchService(http) {
        this.http = http;
    }
    SearchService.prototype.getData = function () {
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
    };
    SearchService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], SearchService);
    return SearchService;
}());
exports.SearchService = SearchService;
//# sourceMappingURL=search.service.js.map