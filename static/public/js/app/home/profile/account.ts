import {Category} from "../search/category";
export class PasswordUpdateDTO {
    old_password: string;
    new_password: string;

    constructor(old_password: string, new_password: string) {
        this.old_password = old_password;
        this.new_password = new_password;
    }
}

export class AccountUpdateDTO {
    username: string;
    first_name: string;
    last_name: string;
    email: string;

    constructor(username: string, first_name: string, last_name: string, email: string) {
        this.username = username;
        this.first_name = first_name;
        this.last_name = last_name;
        this.email = email;
    }
}

export class LocationDTO {
    street: string;
    city: string;
    region: string;
    country: string;

    constructor(street: string, city: string, region: string, country: string) {
        this.street = street;
        this.city = city;
        this.region = region;
        this.country = country;
    }
}

export class Location {
    street: string;
    city: string;
    region: string;
    country: string;

    constructor(street: string, city: string, region: string, country: string) {
        this.street = street;
        this.city = city;
        this.region = region;
        this.country = country;
    }
}

export class Coordinates {
    latitude: number;
    longitude: number;

    constructor(lat: number, lng: number) {
        this.latitude = lat;
        this.longitude = lng;
    }
}

export class OfferGet {
    id: number;
    accepted: boolean;
    answered: boolean;
    comment: string;
    item_given: number;
    item_received: number;

    constructor() {
        this.id = 0;
        this.accepted = false;
        this.answered = false;
        this.comment = "";
        this.item_given = 0;
        this.item_received = 0;
    }
}

export class Account {
    id: number;
    profile_picture_url: string;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    location: Location;
    last_modification_date: string;
    categories: Array<Category>;
    items: Array<number>;
    notes: number;
    note_avg: number;
    coordinates: Coordinates;
    pending_offers: Array<OfferGet>;

    constructor() {
        this.id = null;
        this.profile_picture_url = null;
        this.username = null;
        this.first_name = null;
        this.last_name = null;
        this.email = null;
        this.location = new Location(null, null, null, null);
        this.last_modification_date = null;
        this.categories = [];
        this.items = [];
        this.notes = null;
        this.note_avg = null;
        this.coordinates = new Coordinates(null, null);
        this.pending_offers = [];
    }
}