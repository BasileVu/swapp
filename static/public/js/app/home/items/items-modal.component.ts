import {Component, ViewEncapsulation, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';

import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { ItemsService } from './items.service';
import { AuthService } from '../../shared/authentication/authentication.service';
import { OfferService } from '../offers/offers.service';

import { DetailedItem } from './detailed-item';
import { User } from '../profile/user';
import { Comment } from './comment';
import { CommentCreationDTO } from './comment-creation-dto';
import { Subscription }   from 'rxjs/Subscription';

@Component({
    moduleId: module.id,
    selector: 'items-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items-modal.component.html'
})
export class ItemsModalComponent implements OnInit, OnDestroy {

    loggedIn: boolean;
    user: User;

    item: DetailedItem;
    owner: User;
    ownerItems: Array<DetailedItem>;
    stars: Array<number>;
    comments: Array<Comment> = [];
    subscription: Subscription;

    // Form fields
    private commentForm: FormGroup;
    private commentContent = new FormControl("", Validators.required);

    constructor(private itemsService: ItemsService,
                private authService: AuthService,
                private offerService: OfferService,
                private formBuilder: FormBuilder,
                public toastr: ToastsManager) { }

    ngOnInit() {
        this.item = new DetailedItem(); // Initiate an empty item. hack to avoid errors
        this.owner = new User();
        this.ownerItems = new Array();
        this.stars = new Array();

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                this.loggedIn = loggedIn;
            }
        );

        // Listen for user login
        this.subscription = this.authService.userSelected$.subscribe(
            user => {
                this.user = user;
            }
        );

        // When receiving the detailed item
        this.subscription = this.itemsService.itemSelected$.subscribe(
            item => { 
                this.item = item;

                // Get the owner
                this.itemsService.getUser(item.owner_username)
                    .then(
                        owner => {
                            this.owner = owner;
                            this.fillStars(owner.note_avg);
                            this.ownerItems = [];

                            for (let i in owner.items) {
                                let ownerItem: any = owner.items[i];
                                this.itemsService.getDetailedItem(ownerItem.id).then(
                                    item => {
                                        if (ownerItem.id != item.id)
                                            this.ownerItems.push(item);
                                    },
                                    error => this.toastr.error("Can't get owner's items", "Error")
                                );
                            }
                        },
                        error => this.toastr.error("Can't get the owner", "Error")
                    );

                // Get the comments
                this.itemsService.getComments(item.id)
                    .then(
                        comments => {
                            this.comments = comments
                        },
                        error => this.toastr.error("Can't get the comments", "Error")
                    );
            },
            error => this.toastr.error("Can't get the detailed item", "Error")
        );

        // Initiate the comment form
        this.commentForm = this.formBuilder.group({
            commentContent: this.commentContent
        });
    }

    addComment() {
        if (this.loggedIn) {
            console.log("user");
            console.log(this.user);
            let commentCreationDTO = new CommentCreationDTO(this.user.id, this.item.id, this.commentContent.value);
            console.log(commentCreationDTO);

            this.itemsService.addComment(commentCreationDTO).then(
                res => {
                    console.log(res);
                    this.commentForm.reset();
                    let comment: Comment = new Comment;
                    comment.fromCreationDTO(commentCreationDTO);
                    comment.user_fullname = this.user.first_name + " " + this.user.last_name;
                    comment.user_profile_picture = this.user.profile_picture;
                    comment.date = new Date();
                    comment.id = -1; // TODO : get comment's id from response
                    comment.item = this.item.id;
                    this.comments.push(comment);
                    this.toastr.success("", "Comment submitted");
                },
                error => {
                    console.log(error);
                
                }
            );
        } else {
            this.toastr.error("Please log in to post comments", "Error");
        }
    }

    fillStars(note_avg: number) {
        console.log(note_avg);
        let fullStars = Math.floor(note_avg)
        this.stars = Array(fullStars).fill(1);
        this.stars.push(Math.round( (note_avg % 1) * 2) / 2);
        let size = this.stars.length;
        while (5 - size++ > 0)
            this.stars.push(0);
    }

    searchCategory(category_id: number) {
        console.log("searchCategory id " + category_id);
        // TODO
    }

    swap() {
        console.log("item " + this.item.id + ", owner " + this.owner.id + ", user " + this.user.id);

        this.offerService.openOfferModal([this.user, this.owner, this.item]);
    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
