import {Component, ViewEncapsulation, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';

import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { ItemsService } from './items.service';
import { Item } from "./item";
import { Owner } from "./owner";
import { Comment } from "./comment";
import { CommentCreationDTO } from "./comment-creation-dto";
import { Subscription }   from 'rxjs/Subscription';

@Component({
    moduleId: module.id,
    selector: 'items-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items-modal.component.html'
})
export class ItemsModalComponent implements OnInit, OnDestroy {

    item: Item;
    owner: Owner;
    comments: Array<Comment> = new Array();
    subscription: Subscription;

    // Form fields
    private commentForm: FormGroup;
    private commentContent = new FormControl("", Validators.required);

    constructor(private itemsService: ItemsService,
                private formBuilder: FormBuilder,
                public toastr: ToastsManager) { }

    ngOnInit() {
        this.item = new Item(); // Initiate an empty item. hack to avoid errors
        this.owner = new Owner();
        this.subscription = this.itemsService.itemSelected$.subscribe(
            item => this.item = item
        );
        this.commentForm = this.formBuilder.group({
            commentContent: this.commentContent
        });
    }

    addComment() {
        let commentCrationDTO = new CommentCreationDTO(1, this.item.id, this.commentContent.value); // TODO proper user id
        console.log(commentCrationDTO);

        this.itemsService.addComment(commentCrationDTO).then(
            res => {
                console.log(res);
                this.commentForm.reset();
                let comment: Comment = new Comment;
                comment.fromCreationDTO(commentCrationDTO);
                comment.setUsername(""); // TODO
                comment.setUserProfilePictureUrl(""); // TODO
                this.comments.push(comment);
                this.toastr.success("", "Comment submitted");
            },
            error => {
                console.log(error);
            }
        );
    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
