export class InventoryItem {
    url: string;
    name: string;
    image: string;
    creation_date: Date;

    constructor(url: string, name: string, image: string, creation_date: Date) {
        this.url = url;
        this.name = name;
        this.image = image;
        this.creation_date = creation_date;
    }
}