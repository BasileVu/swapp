import {Component, ViewEncapsulation, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, FormBuilder }  from '@angular/forms';
import { __platform_browser_private__,
    DomSanitizer } from '@angular/platform-browser';

import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { ItemsService } from './items.service';
import { AuthService } from '../../shared/authentication/authentication.service';
import { OfferService } from '../offers/offers.service';

import { DetailedItem } from './detailed-item';
import {User} from '../profile/user';
import { Comment } from './comment';
import { CommentCreationDTO } from './comment-creation-dto';
import { Subscription }   from 'rxjs/Subscription';
import {Like} from "./like";
import {InventoryItem} from "../inventory/inventory-item";

declare let $: any;

@Component({
    moduleId: module.id,
    selector: 'items-modal',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './items-modal.component.html',
    styles:[`
        .big-pic {
            max-width: 100%;
            max-height: 500px;
        }
        
        .small-pic {
            max-width: 100%;
            max-height: 250px;
        }
    `],
    providers: [__platform_browser_private__.BROWSER_SANITIZATION_PROVIDERS]
})
export class ItemsModalComponent implements OnInit, OnDestroy {

    loggedIn: boolean;
    user: User = new User;

    item: DetailedItem;
    owner: User;
    ownerItems: Array<InventoryItem>;
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
                private sanitizer: DomSanitizer,
                public toastr: ToastsManager) {console.log("construcot"); }

    ngOnInit() {
        this.item = new DetailedItem(); // Initiate an empty item. hack to avoid errors
        this.owner = new User();
        this.ownerItems = [];
        this.stars = [];

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
                for (let userInventoryItem of this.item.similar)
                    this.sanitizer.bypassSecurityTrustUrl(userInventoryItem.image_url);

                console.log(this.item);
                // Get the owner
                this.itemsService.getUser(item.owner_username)
                    .then(
                        owner => {
                            this.owner = owner;
                            this.fillStars(owner.note_avg);
                            this.ownerItems = [];

                            for (let inventoryItem of owner.items) {
                                this.sanitizer.bypassSecurityTrustUrl(inventoryItem.image_url);
                                if (inventoryItem.id != item.id)
                                    this.ownerItems.push(inventoryItem);
                            }
                        },
                        error => this.toastr.error("Can't get the owner", "Error")
                    );

                // Get the comments
                this.itemsService.getComments(item.id)
                    .then(
                        comments => {
                            this.comments = comments;
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

        // on close, destroy flickity carousal
        $('#view-item-x').on('hide.bs.modal', function (e: any) {
            $('.modal-carousel').flickity('destroy');
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
                    comment.user_profile_picture = this.user.profile_picture_url;
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
        let fullStars = Math.floor(note_avg);
        this.stars = Array(fullStars).fill(1);
        this.stars.push(Math.round( (note_avg % 1) * 2) / 2);
        let size = this.stars.length;
        while (5 - size++ > 0)
            this.stars.push(0);
    }

    searchCategory(category: any) {
        this.toastr.warning("for this '" + this.item.name + "' (TODO)", "Search '" + category.name + "'");
        // TODO
    }

    swap() {
        this.offerService.openOfferModal([this.user, this.owner, this.item]);
    }

    signalFraud() {
        this.toastr.warning("for this '" + this.item.name + "' (TODO)", "Fraud signaled");
        // TODO
    }

    security() {
        this.toastr.warning("for this '" + this.item.name + "' (TODO)", "Security");
        // TODO
    }

    sendMessage() {
        this.toastr.warning("to '" + this.owner.first_name + " " + this.owner.last_name + "' (TODO)", "Send message");
        // TODO
    }

    writeComment() {
        this.toastr.warning("for this '" + this.item.name + "' (TODO)", "Write a comment");
        // TODO
    }

    openProfileModal() {
        this.toastr.warning("TODO (profile modal subscribed and we signal the profile)", "Open profile");
        // TODO : voir avec Mathieu
    }

    seeMore() {
        this.toastr.warning("for this '" + this.item.name + "' (TODO)", "See more");
        // TODO
    }

    like() {
        let l = new Like();
        l.date = new Date().toISOString();
        l.item = this.item.id;
        l.user = this.user.id;

        this.itemsService.like(l).then(
            res => this.toastr.success("'" + this.item.name + "'", "Liked"),
            error => this.toastr.error(error, "Error")
        )
    }

    shareItem() {

    }

    ngOnDestroy() {
        // prevent memory leak when component is destroyed
        this.subscription.unsubscribe();
    }
}
