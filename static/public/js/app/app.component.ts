import {Component, OnInit, AfterViewInit, ViewContainerRef,
    trigger,
    state,
    style,
    transition,
    animate,
} from '@angular/core';

import './rxjs-operators';
import { Http } from "@angular/http";
import { Subscription }   from 'rxjs/Subscription';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { AuthService } from './shared/authentication/authentication.service';
import {Account} from "./home/profile/account";

declare let $:any;
declare let google: any;

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: 'app.component.html',
    animations: [
        trigger('flyInOut', [
            state('in', style({opacity: 1, transform: 'translateX(0)'})),
            transition('void => *', [
                style({
                    opacity: 0,
                    transform: 'translateX(-100%)'
                }),
                animate('0.2s ease-in')
            ]),
            transition('* => void', [
                animate('0.2s 10 ease-out', style({
                    opacity: 0,
                    transform: 'translateX(100%)'
                }))
            ])
        ])
    ]
})
export class AppComponent implements OnInit, AfterViewInit {
    loggedIn: boolean = false;
    subscription: Subscription;
    account: Account = new Account();

    constructor (private http: Http,
                 private authService: AuthService,
                 public toastr: ToastsManager, vRef: ViewContainerRef) {
        this.toastr.setRootViewContainerRef(vRef);
    }

    ngOnInit() {
        this.authService.getCSRF();

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => {
                this.loggedIn = loggedIn;
                if (this.loggedIn)
                    this.seeProfile();
            }
        );

        // TODO : make a proper service to store geolocation
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(position) {
                localStorage.setItem("latitude", String(position.coords.latitude));
                localStorage.setItem("longitude", String(position.coords.longitude));
            });
        } else {
            console.log("Geolocation not available");
        }
    }

    seeProfile() {
        this.authService.getAccount().then(
            account => {
                this.account = account;
            },
            error => this.toastr.error(error, "Error")
        )
    }

    logout() {
        this.authService.logout()
            .then(
                res => {
                    this.loggedIn = false;
                    this.toastr.success("", "Logged out");

                    // Delete the cookie and get a new one for not authenticated queries
                    localStorage.removeItem("connected");
                    this.deleteCookie('csrftoken');
                    this.authService.getCSRF().then(
                        res => {
                            // Announce the item component to get a new set of items
                            // (for a user not logged in)
                            this.authService.selectLoggedIn(this.loggedIn);
                        },
                        error => console.log(error)
                    );
                },
                error => {
                    console.log(error);
                }
            );
    }

    deleteCookie(name: string) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    
    ngAfterViewInit() {

        let that = this;
        setTimeout(function() {

            that.loggedIn = localStorage.getItem("connected") === "true";
            if (that.loggedIn)
                that.authService.selectLoggedIn(that.loggedIn);

            $('document').ready(function() {

                $('.grid').isotope({
                    // options
                    itemSelector: '.grid-item',
                    layoutMode: 'masonry'
                });

                /*
                 TODO : remove because it's handled in update-inventory.directive.ts
                // home inventory ///////////////////////////
                let inventory = $('.home-inventory').flickity({
                    // options
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    groupCells: '100%',
                    prevNextButtons: false,
                    adaptiveHeight: true
                });
                */

                // Home link reload page
                $(".home-link").click(function(){
                    location.reload();
                });

                // open user creation modal /////////////////////
                let openCreateProfileButtons = $('.open-create-profile-modal');
                let createProfileModal = $('#create-user-modal');
                openCreateProfileButtons.each(function () {
                    $(this).click(function () {
                        createProfileModal.modal('show');
                    });
                });

                // open item creation modal /////////////////////
                let addItemButtons = $('.open-new-item-modal');
                let newItemModal = $('#add-item-modal');
                addItemButtons.each(function () {
                    $(this).click(function () {
                        newItemModal.modal('show');
                    });
                });

                // open send proposition modal /////////////////////
                let openSendPropositionButtons = $('.open-send-proposition-modal');
                let sendPropositionModal = $('#send-proposition-modal');
                openSendPropositionButtons.each(function () {
                    $(this).click(function () {
                        sendPropositionModal.modal('show');
                    });
                });

                // open infos modal ////////////////////////
                $('.open-modal-infos').click(function () {
                    $('#view-infos').modal('show');
                });

                // open messages modal ////////////////////////
                $('.open-messages-modal').click(function () {
                    $('#view-messages').modal('show');
                });

                // display item modal ///////////////////////////
                let theItemModal = $('#view-item-x');
                let theEditItemModal = $('#edit-item-modal');
                // show.bs.modal would be better, but not working in bootstrap 4 alpha 4
                theItemModal.on('show.bs.modal', function (e: any) {
                    // modal slider ///////////////////////////
                    let modalCarousel = $('.modal-carousel').flickity({
                        cellAlign: 'center',
                        contain: true,
                        imagesLoaded: true,
                        wrapAround: true,
                        prevNextButtons: false,
                        adaptiveHeight: true
                    });

                    setTimeout(function () {
                        modalCarousel.flickity('resize');
                        $('.modal-carousel-height').matchHeight({
                            byRow: false,
                            target: modalCarousel
                        });
                    }, 300)
                });
                $('.open-modal-item-x').click(function () {
                    theItemModal.modal('show');
                });
                $('.open-modal-edit-item-x').click(function () {
                    theEditItemModal.modal('show');
                });

                // advanced search ///////////////////////////
                let advancedSearchModal = $('#advanced-search-modal');
                $('.open-modal-advanced-search').click(function () {
                    advancedSearchModal.modal('show');
                });
            });

        }, 0);
        
    }
}