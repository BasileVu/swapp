import { KeyInfo } from './key-info';

export class ItemCreationDTO {
    name: string;
    description: string;
    price_min: number;
    price_max: number;
    category: number;
    keyinfo_set: Array<KeyInfo>;
    delivery_methods: Array<number>;

    constructor(name: string,
                price_min: number,
                price_max: number,
                category: number,
                description: string,
                keyinfo_set: Array<KeyInfo>,
                delivery_methods: Array<number>) {
        this.name = name;
        this.description = description;
        this.price_min = price_min;
        this.price_max = price_max;
        this.category = category;
        this.keyinfo_set = keyinfo_set;
        this.delivery_methods = delivery_methods
    }
}