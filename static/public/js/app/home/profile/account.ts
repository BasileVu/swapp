class Location {
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
export class Account {
    id: number;
    profile_picture_url: string;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    location: Location;
    last_modification_date: string;
    categories: Array<string>;
    items: Array<number>;
    notes: number;
    note_avg: number;

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
    }
}