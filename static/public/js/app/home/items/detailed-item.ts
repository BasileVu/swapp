class KeyInfo {
    key: string;
    value: string;
}


export class DetailedItem {
    id: number;
    name: string;
    description: string;
    price_min: number;
    price_max: number;
    creation_date: Date;
    keyinfo_set: Array<KeyInfo>;
    owner_username: string;
    category: {
        id: number;
        name: string;
    };
    views: number;

    // TODO : missing in API endpoint GET /items/
    delivery_methods: Array<string>;
    owner_profile_picture_url: string;
    //

    image_urls: Array<string>; // other images
    likes: number;
    comments: number;
    offers_received: number;
    similar: Array<{
        id: number;
        name: string;
        image_url: string;
    }>;

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
        this.owner_profile_picture_url = null;
    }

    getId(): number {
        return this.id;
    }
}
