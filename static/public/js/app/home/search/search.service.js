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
var SearchService = (function () {
    function SearchService(http) {
        this.http = http;
        this.categoriesUrl = '/api/categories/'; // URL to web API
        this.itemsUrl = '/api/items/';
    }
    SearchService.prototype.getCategories = function () {
        return this.http.get(this.categoriesUrl)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    };
    SearchService.prototype.search = function (search) {
        var params = new http_1.URLSearchParams();
        params.set('q', search.q);
        params.set('category', search.category);
        params.set('order_by', search.orderBy);
        return this.http.get(this.itemsUrl, { search: params })
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    };
    SearchService.prototype.extractData = function (res) {
        var body = res.json();
        return body || {};
    };
    SearchService.prototype.handleError = function (error) {
        // In a real world app, we might use a remote logging infrastructure
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
    return SearchService;
}());
SearchService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Http])
], SearchService);
exports.SearchService = SearchService;
//# sourceMappingURL=search.service.js.map