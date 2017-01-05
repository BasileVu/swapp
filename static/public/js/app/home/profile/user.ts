export class UserInventoryItem {
    id: number;
    image_url: string;
    name: string;

    constructor() {
        this.id = null;
        this.image_url = null;
        this.name = null;
    }
}

export class User {
    id: number;
    profile_picture: string;
    username: string;
    first_name: string;
    last_name: string;
    location: string;
    items: Array<UserInventoryItem>;
    notes: number;
    note_avg: number;

    constructor() {
        this.id = -1;
        this.profile_picture = "";
        this.username = "";
        this.first_name = "";
        this.last_name = "";
        this.location = "";
        this.items = [];
        this.notes = 0;
        this.note_avg = 0;
    }
}