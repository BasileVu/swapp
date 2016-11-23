import { Injectable } from '@angular/core';

export class User {
    constructor(
        public email: string,
        public password: string) { }
}

// TODO : check on backend
var users = [
    new User('admin@admin.com', 'adm9'),
    new User('user1@gmail.com', 'a23')
];

@Injectable()
export class AuthService {

    constructor() { }

    logout() {
        localStorage.removeItem("user");
    }
    
    login(username, password) {
        /*var authenticatedUser = users.find(u => u.email === user.email);
        if (authenticatedUser && authenticatedUser.password === user.password) {
            localStorage.setItem("user", authenticatedUser);
            return true;
        }*/
        return false;
    }

    checkCredentials() {
        //return localStorage.getItem("user") !== null;
        return true;
    }
}