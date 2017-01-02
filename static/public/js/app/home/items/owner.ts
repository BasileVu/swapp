export class Owner {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    profile_picture_url: string;
    location: string;
    items: Array<number>;
    note_avg: number;
    votes: number;
    interested_in: Array<string>;
    delivery_address: string;
    delivery_methods: Array<string>;

    constructor() {
        this.id = -1;
        this.first_name = "undef";
        this.last_name = "undef";
        this.username = "undef";
        this.profile_picture_url = "undef";
        this.items = new Array();
        this.votes = 0;
        this.note_avg = 0;
        this.interested_in = new Array();
        this.delivery_address = "undef";
        this.delivery_methods = new Array();
    }
}