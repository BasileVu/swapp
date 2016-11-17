export class Item {
    id: number;
    name: string;
    description: string;
    price_min: number;
    price_max: number;
    creation_date: Date;
    archived: boolean;
    owner: number;
    category: number;

    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}
