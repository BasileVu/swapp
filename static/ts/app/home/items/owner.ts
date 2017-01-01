export class Owner {
    id: number;
    first_name: string;
    last_name: string;
    username: string;
    profile_picture_url: string;
    inventory: Array<{
        item_id: number;
        image_url: string;
    }>;
    score: number;
    number_of_vote: number;
    interested_in: Array<string>;
    delivery_address: string;
    delivery_methods: Array<string>;

    constructor() {
        this.id = -1;
        this.first_name = "undef";
        this.last_name = "undef";
        this.username = "undef";
        this.profile_picture_url = "undef";
        this.inventory = new Array();
        this.score = 0;
        this.number_of_vote = 0;
        this.interested_in = new Array();
        this.delivery_address = "undef";
        this.delivery_methods = new Array();
    }
}