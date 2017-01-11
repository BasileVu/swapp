export class OfferUpdate {
    accepted: boolean;
    comment: string;

    constructor(accepted: boolean, comment: string) {
        this.accepted = accepted;
        this.comment = comment;
    }
}