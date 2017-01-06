import {UserInventoryItem} from "../profile/user";
class KeyInfo {
    key: string;
    info: string;
}


export class DetailedItem {
    id: number;
    name: string;
    description: string;
    price_min: number;
    price_max: number;
    creation_date: Date;
    keyinfo_set: Array<KeyInfo>;
    delivery_methods: Array<{id:number, name:string}>;
    category: {
        id: number;
        name: string;
    };
    views: number;
    image_urls: Array<string>; // other images
    likes: number;
    comments: number;
    offers_received: number;
    similar: Array<UserInventoryItem>;
    owner_username: string;
    owner_picture_url: string;
    owner_location: string;

    constructor() {
        this.id = -1;
        this.name = undefined;
        this.description = undefined;
        this.image_urls = [];
        this.price_min = -1;
        this.price_max = -1;
        this.keyinfo_set = [];
        this.creation_date = new Date();
        this.offers_received = 0;
        this.views = 0;
        this.likes = 0;
        this.comments = 0;
        this.owner_username = "";
        this.category = {id:-1, name:undefined};
        this.similar = [];
        this.owner_username = "";
        this.owner_picture_url = null;
        this.owner_location = "";
        this.delivery_methods = [];
    }
}
