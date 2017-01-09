export class OfferUpdate {
    accepted: boolean;
    answered: boolean;

    constructor(accepted: boolean, answered: boolean) {
        this.accepted = accepted;
        this.answered = answered;
    }
}