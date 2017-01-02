import { KeyInfo } from './key-info';

export class ItemCreationDTO {
    url: string;
    username: string;
    name: string;
    price_min: number;
    price_max: number;
    category: string;
    description: string;
    key_informations: Array<KeyInfo>;
    images: Array<string>;
    image_set: Array<number> = new Array(); // // TODO : still needed ? check with api
    owner_interests: Array<string>;
    accepted_delivery_ids: Array<string>;
    creation_date: Date;
    like_set: Array<string> = new Array(); // TODO : still needed ? check with api

    constructor(username: string,
                name: string,
                price_min: number,
                price_max: number,
                category: string,
                description: string,
                key_informations: Array<KeyInfo>,
                images: Array<string>,
                owner_interests: Array<string>,
                accepted_delivery_ids: Array<string>,
                creation_date: Date) {
        this.username = username;
        this.name = name;
        this.price_min = price_min;
        this.price_max = price_max;
        this.category = category;
        this.description = description;
        this.key_informations = key_informations;
        this.images = images;
        this.owner_interests = owner_interests;
        this.accepted_delivery_ids = accepted_delivery_ids;
        this.creation_date = creation_date;  
    }

    setUrl(url: string) {
        this.url = url;
    }
}