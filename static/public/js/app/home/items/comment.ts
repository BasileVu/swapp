import { CommentCreationDTO } from './comment-creation-dto';

export class Comment {
    user_id: number;
    user_profile_picture_url: string;
    user_fullname: string;
    date: Date;
    content: string;

    fromCreationDTO(commentCreationDTO: CommentCreationDTO) {
        this.user_id = commentCreationDTO.user;
        this.content = commentCreationDTO.content;
    }

    setUserFullname(user_fullname: string) {
        this.user_fullname = user_fullname;
    }

    setUserProfilePictureUrl(picture: string) {
        this.user_profile_picture_url = picture;
    }

    setDate(date: Date) {
        this.date = date;
    }
}