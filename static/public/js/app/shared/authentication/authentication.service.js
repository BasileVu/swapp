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
var Subject_1 = require('rxjs/Subject');
var AuthService = (function () {
    function AuthService(http) {
        this.http = http;
        // Observable source
        this.loggedInSelectedSource = new Subject_1.Subject();
        // Observable boolean streams
        this.loggedInSelected$ = this.loggedInSelectedSource.asObservable();
        this.loggedIn = false;
    }
    // Service message commands
    AuthService.prototype.selectLoggedIn = function (loggedIn) {
        this.loggedInSelectedSource.next(loggedIn);
    };
    AuthService.prototype.isLoggedIn = function () {
        return this.loggedIn;
    };
    AuthService.prototype.logout = function () {
        localStorage.removeItem("user");
    };
    AuthService.prototype.login = function (username, password) {
        var body = JSON.stringify({ username: username, password: password }); // Stringify payload
        var headers = new http_1.Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        var options = new http_1.RequestOptions({ headers: headers }); // Create a request option
        // No content to return, we just catch errors
        return this.http.post('/api/login/', body, options)
            .toPromise()
            .catch(this.handleError);
    };
    /*
        private extractData(res: Response) {
            console.log("Response: " + res);
            let body = res.json();
            return body || { };
        }
    */
    AuthService.prototype.handleError = function (error) {
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
        console.error("error: " + errMsg);
        return Promise.reject(errMsg);
    };
    AuthService.prototype.checkCredentials = function () {
        //return localStorage.getItem("user") !== null;
        return true;
    };
    AuthService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], AuthService);
    return AuthService;
}());
exports.AuthService = AuthService;
//# sourceMappingURL=authentication.service.js.map