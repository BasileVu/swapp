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

    constructor(profile_picture: string,
                username: string,
                first_name: string,
                last_name: string,
                email: string,
                street: string,
                city: string,
                region: string,
                country: string,
                last_modification_date: string,
                notes: Array<number>,
                likes: Array<number>,
                items: Array<number>) {
        this.profile_picture = profile_picture;
        this.username = username;
        this.first_name = first_name;
        this.last_name = last_name;
        this.email = email;
        this.location = new Location(street, city, region, country);
        this.last_modification_date = new Date(last_modification_date);
        this.notes = notes;
        this.likes = likes;
        this.items = items;
    }
}