class Like {
    id: number;
    user: number;
}

export class Item {
    id: number;
    name: string;
    description: string;
    image_url: string; // main image
    image_set: Array<string>; // other images
    price_min: number;
    price_max: number;
    key_informations: Array<{
        key: string,
        value: string
    }>;
    creation_date: Date;
    city: string;
    country: string;
    offers_received: number;
    views: number;
    likes: number;
    comments: number;

    owner: number;
    owner_image_url: string;
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
        this.name = "undef";
        this.description = "undef";
        this.image_url = "undef";
        this.image_set = new Array();
        this.price_min = -1;
        this.price_max = -1;
        this.key_informations = new Array();
        this.creation_date = new Date();
        this.city = "undef";
        this.country = "undef";
        this.offers_received = 0;
        this.views = 0;
        this.likes = 0;
        this.comments = 0;
        this.owner = -1;
        this.owner_image_url = "undef";
        this.category = {id:-1, name:"undef"};
        this.similars = new Array();
    }

    getId(): number {
        return this.id;
    }
}
