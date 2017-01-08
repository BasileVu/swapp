export class InventoryItem {
    id: number;
    name: string;
    image_id: number;
    image_url: string;
    archived: boolean;

    constructor(id: number, name: string, image_id: number, image_url: string, archived: boolean) {
        this.id = id;
        this.name = name;
        this.image_id = image_id;
        this.image_url = image_url;
        this.archived = archived;
    }
}