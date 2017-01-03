export class DetailedItem {
    owner_username: string;
    id: number;
    name: string;
    description: string;
    image_urls: Array<string>; // other images
    price_min: number;
    price_max: number;
    creation_date: Date;
    interested_by: Array<string>;
    key_informations: Array<{
        key: string,
        value: string
    }>;
    delivery_from: string;
    delivery_methods: Array<string>;
    offers_received: number;
    comments: number;
    views: number;
    likes: number;
    category: {
        id: number;
        name: string;
    };
    similars: Array<{
        item_id: string;
        image_url: string;
    }>;

    constructor() {
        this.id = -1;
        this.name = undefined;
        this.description = undefined;
        this.image_urls = new Array();
        this.price_min = -1;
        this.price_max = -1;
        this.key_informations = new Array();
        this.creation_date = new Date();
        this.offers_received = 0;
        this.views = 0;
        this.likes = 0;
        this.comments = 0;
        this.owner_username = "";
        this.category = {id:-1, name:undefined};
        this.similars = new Array();
    }

    getId(): number {
        return this.id;
    }
}
