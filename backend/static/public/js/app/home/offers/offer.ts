export class Offer {
    accepted: boolean;
    answered: boolean;
    comment: string;
    item_given: number;
    item_received: number;

    constructor() {
        this.accepted = false;
        this.answered = false;
        this.comment = "";
        this.item_given = -1;
        this.item_received = -1;
    }
}