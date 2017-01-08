import {InventoryItem} from "../inventory/inventory-item";

export class User {
    id: number;
    profile_picture_url: string;
    username: string;
    first_name: string;
    last_name: string;
    location: string;
    items: Array<InventoryItem>;
    notes: number;
    note_avg: number;
    interested_by: Array<{id:number,name:string}>;

    constructor() {
        this.id = -1;
        this.profile_picture_url = null;
        this.username = "";
        this.first_name = "";
        this.last_name = "";
        this.location = "";
        this.items = [];
        this.notes = 0;
        this.note_avg = 0;
        this.interested_by = [];
    }
}