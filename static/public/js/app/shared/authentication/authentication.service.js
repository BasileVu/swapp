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
var User = (function () {
    function User(email, password) {
        this.email = email;
        this.password = password;
    }
    return User;
}());
exports.User = User;
// TODO : check on backend
var users = [
    new User('admin@admin.com', 'adm9'),
    new User('user1@gmail.com', 'a23')
];
var AuthService = (function () {
    function AuthService() {
    }
    AuthService.prototype.logout = function () {
        localStorage.removeItem("user");
    };
    AuthService.prototype.login = function (username, password) {
        /*var authenticatedUser = users.find(u => u.email === user.email);
        if (authenticatedUser && authenticatedUser.password === user.password) {
            localStorage.setItem("user", authenticatedUser);
            return true;
        }*/
        return false;
    };
    AuthService.prototype.checkCredentials = function () {
        //return localStorage.getItem("user") !== null;
        return true;
    };
    AuthService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [])
    ], AuthService);
    return AuthService;
}());
exports.AuthService = AuthService;
//# sourceMappingURL=authentication.service.js.map