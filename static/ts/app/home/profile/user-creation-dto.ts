export class UserCreationDTO {
    username: string;
    email: string;
    password: string;
    confirmPassword: string;
    first_name: string;
    last_name: string;
    address: string;
    city: string;
    region: string;
    country: string;
    picture: string;

    constructor(username: string,
                email: string,
                password: string,
                confirmPassword: string,
                firstname: string,
                lastname: string,
                address: string,
                city: string,
                region: string,
                country: string,
                picture: string) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.confirmPassword = confirmPassword;
        this.first_name = firstname;
        this.last_name = lastname;
        this.address = address;
        this.city = city;
        this.region = region;
        this.country = country;
        this.picture = picture;
    }
}