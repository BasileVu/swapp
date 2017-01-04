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

export class User {
    id: number;
    profile_picture: string;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    location: Location;
    last_modification_date: Date;
    notes: Array<number>;
    likes: Array<number>;
    items: Array<number>;


    constructor() {
        this.id = -1;
        this.profile_picture = "";
        this.username = "";
        this.first_name = "";
        this.last_name = "";
        this.email = "";
        this.location = new Location("", "", "", "");
        this.last_modification_date = new Date();
        this.notes = [];
        this.likes = [];
        this.items = [];
    }
}