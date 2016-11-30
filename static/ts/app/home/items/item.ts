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


    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}
