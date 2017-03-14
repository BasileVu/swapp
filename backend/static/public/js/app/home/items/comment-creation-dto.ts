export class CommentCreationDTO {
    user: number;
    item: number;
    content: string;

    constructor(user: number, item: number, content: string) {
        this.user = user;
        this.item = item;
        this.content = content;
    }
}