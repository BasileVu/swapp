export class InventoryItem {
    id: number;
    name: string;
    image: string;
    creation_date: Date;

    constructor(id: number, name: string, image: string, creation_date: Date) {
        this.id = id;
        this.name = name;
        this.image = image;
        this.creation_date = creation_date;
    }
}