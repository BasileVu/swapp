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
var core_1 = require("@angular/core");
var http_1 = require("@angular/http");
var Subject_1 = require("rxjs/Subject");
var ItemsService = (function () {
    function ItemsService(http) {
        this.http = http;
        // Observable string sources
        this.itemSelectedSource = new Subject_1.Subject();
        this.ownerSelectedSource = new Subject_1.Subject();
        this.commentsSelectedSource = new Subject_1.Subject();
        // Observable string streams
        this.itemSelected$ = this.itemSelectedSource.asObservable();
        this.ownerSelected$ = this.ownerSelectedSource.asObservable();
        this.commentsSelected$ = this.commentsSelectedSource.asObservable();
        this.itemsSubject = new Subject_1.Subject();
        this.itemsUrl = '/api/items/'; // URL to web API
    }
    // Service message commands
    ItemsService.prototype.selectItem = function (item) {
        this.itemSelectedSource.next(item);
    };
    ItemsService.prototype.selectOwner = function (owner) {
        this.ownerSelectedSource.next(owner);
    };
    ItemsService.prototype.selectComments = function (comments) {
        this.commentsSelectedSource.next(comments);
    };
    ItemsService.prototype.updateItems = function (items) {
        this.itemsSubject.next(items);
    };
    ItemsService.prototype.getItemsSubject = function () {
        return this.itemsSubject.asObservable();
    };
    ItemsService.prototype.getItems = function () {
        return this.http.get(this.itemsUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    };
    ItemsService.prototype.getItem = function (id) {
        return this.http.get(this.itemsUrl + id)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    };
    ItemsService.prototype.getOwner = function (owner_id) {
        return this.http.get('/api/users/' + owner_id)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    };
    ItemsService.prototype.getComments = function (item_id) {
        return this.http.get(this.itemsUrl + item_id + '/comments')
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    };
    ItemsService.prototype.extractData = function (res) {
        var body = res.json();
        return body || {};
    };
    ItemsService.prototype.handleError = function (error) {
        // TODO : In a real world app, we might use a remote logging infrastructure
        var errMsg;
        if (error instanceof http_1.Response) {
            var body = error.json() || '';
            var err = body.error || JSON.stringify(body);
            errMsg = error.status + " - " + (error.statusText || '') + " " + err;
        }
        else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Promise.reject(errMsg);
    };
    return ItemsService;
}());
ItemsService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Http])
], ItemsService);
exports.ItemsService = ItemsService;
//# sourceMappingURL=items.service.js.map