import { CommentCreationDTO } from './comment-creation-dto';

export class Comment {
    id: number;
    content: string;
    date: Date;
    user: number;
    item: number;
    user_fullname: string;
    user_profile_picture: string;

    constructor() {
        this.id = null;
        this.content = null;
        this.date = null;
        this.user = null;
        this.item = null;
        this.user_fullname = null;
        this.user_profile_picture = null;
    }

    fromCreationDTO(commentCreationDTO: CommentCreationDTO) {
        this.user = commentCreationDTO.user;
        this.content = commentCreationDTO.content;
    }
}