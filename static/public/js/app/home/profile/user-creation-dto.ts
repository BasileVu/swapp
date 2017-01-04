export class UserCreationDTO {
    username: string;
    email: string;
    password: string;
    password_confirmation: string;
    first_name: string;
    last_name: string;
    street: string;
    city: string;
    region: string;
    country: string;
    
    constructor(username: string,
                email: string,
                password: string,
                password_confirmation: string,
                firstname: string,
                lastname: string,
                street: string,
                city: string,
                region: string,
                country: string) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.password_confirmation = password_confirmation;
        this.first_name = firstname;
        this.last_name = lastname;
        this.street = street;
        this.city = city;
        this.region = region;
        this.country = country;
    }
}