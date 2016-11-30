class Image {
    id: number;
    image: string;
}

class Like {
    id: number;
    user: number;
}

export class Item {
    id: number;
    name: string;
    description: string;
    price_min: number;
    price_max: number;
    creation_date: Date;
    archived: boolean;
    owner: {
        id: number,
        profile_picture: string,
        location: string
    };
    category: {
        id: number,
        name: string
    };
    image_set: Image[];
    like_set: Like[];

    constructor() {
        this.id = -1;
        this.name = "undef";
        this.description = "undef";
        this.price_min = -1;
        this.price_max = -1;
        this.creation_date = new Date();
        this.archived = false;
        this.owner = {id: -1, profile_picture: "undef", location:"undef"};
        this.category = {id:-1, name:"undef"};
    }

    getId(): number {
        return this.id;
    }
}
