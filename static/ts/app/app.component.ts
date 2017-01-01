import {Component, OnInit, AfterViewInit, ViewContainerRef,
    trigger,
    state,
    style,
    transition,
    animate,
    keyframes,
} from '@angular/core';

import './rxjs-operators';
import { Http } from "@angular/http";
import { Subscription }   from 'rxjs/Subscription';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

import { AuthService } from './shared/authentication/authentication.service';

declare var $:any;
declare var google: any;

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
    subtitle = '(v1)';

    loggedIn: boolean;
    subscription: Subscription;

    constructor (private http: Http,
                 private authService: AuthService,
                 public toastr: ToastsManager, vRef: ViewContainerRef) {
        this.toastr.setRootViewContainerRef(vRef);
    }

    ngOnInit() {
        let csrf = this.http.get("/api/csrf/");

        this.loggedIn = this.authService.isLoggedIn();

        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(
            loggedIn => this.loggedIn = loggedIn
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

    logout() {
        this.authService.logout()
            .then(
                res => {
                    if (res.status === 200) {
                        this.loggedIn = false;
                        this.authService.selectLoggedIn(this.loggedIn);
                        this.toastr.success("", "Logged out");
                    }
                },
                error => {
                    console.log(error);
                }
            );
    }
    
    ngAfterViewInit() {

        setTimeout(function() {
            $('document').ready(function() {
                
                // home grid ///////////////////////////
                var grid = $('.grid').isotope({
                    // options
                    itemSelector: '.grid-item',
                    layoutMode: 'masonry'
                });
                // layout only when images are loaded
                grid.imagesLoaded().progress( function() {
                    grid.isotope('layout');
                });
                // display items details when hovered
                $('.grid-item').hover(function () {
                    $(this).addClass('hovered');
                    grid.isotope('layout');
                }, function () {
                    $(this).removeClass('hovered');
                    grid.isotope('layout');
                });

                // home inventory ///////////////////////////
                var inventory = $('.home-inventory').flickity({
                    // options
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    groupCells: '100%',
                    prevNextButtons: false,
                    adaptiveHeight: true
                });

                // swapp inventories /////////////////////////
                var swapp_inventory_mine = $('.swapp-inventory-mine').flickity({
                    // options
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    groupCells: '100%',
                    prevNextButtons: false,
                    adaptiveHeight: true,
                    pageDots: true
                });
                var swapp_inventory_yours = $('.swapp-inventory-yours').flickity({
                    // options
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    groupCells: '100%',
                    prevNextButtons: false,
                    adaptiveHeight: true,
                    pageDots: true
                });

                // modal slider ///////////////////////////
                var modalCarousel = $('.modal-carousel').flickity({
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    prevNextButtons: false,
                    adaptiveHeight: true
                });

                var modalCarouselNav = $('.modal-carousel-nav');
                var modalCarouselNavCells = modalCarouselNav.find('.carousel-cell');

                modalCarouselNav.on( 'click', '.carousel-cell', function( event ) {
                    var index = $( event.currentTarget ).index();
                    modalCarousel.flickity( 'select', index );
                });

                var flkty = modalCarousel.data('flickity');
                var navCellHeight = modalCarouselNavCells.height();
                var navHeight = modalCarouselNav.height();

                modalCarousel.on( 'select.flickity', function() {
                    // set selected nav cell
                    modalCarouselNav.find('.is-nav-selected').removeClass('is-nav-selected');
                    var selected = modalCarouselNavCells.eq( flkty.selectedIndex )
                        .addClass('is-nav-selected');
                    // scroll nav
                    var scrollY = selected.position().top +
                        modalCarouselNav.scrollTop() - ( navHeight + navCellHeight ) / 2;
                    modalCarouselNav.animate({
                        scrollTop: scrollY
                    });
                });

                // open user creation profile modal /////////////////////
                var openCreateProfileButtons = $('.open-create-profile-modal');
                var createProfileModal = $('#create-user-modal');
                openCreateProfileButtons.each(function () {
                    $(this).click(function () {
                        createProfileModal.modal('show');
                    });
                });

                // open item creation modal /////////////////////
                var addItemButtons = $('.open-new-item-modal');
                var newItemModal = $('#add-item-modal');
                addItemButtons.each(function () {
                    $(this).click(function () {
                        newItemModal.modal('show');
                    });
                });

                // open send proposition modal /////////////////////
                var openSendPropositionButtons = $('.open-send-proposition-modal');
                var sendPropositionModal = $('#send-proposition-modal');
                openSendPropositionButtons.each(function () {
                    $(this).click(function () {
                        sendPropositionModal.modal('show');
                    });
                });
                sendPropositionModal.on('show.bs.modal', function (e) {
                    setTimeout(function () {
                        swapp_inventory_mine.flickity('resize');
                        swapp_inventory_yours.flickity('resize');
                    }, 300)
                });

                // display item modal ///////////////////////////
                var theItemModal = $('#view-item-x');
                // show.bs.modal would be better, but not working in bootstrap 4 alpha 4
                theItemModal.on('show.bs.modal', function (e) {
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

                // advanced search ///////////////////////////
                var advancedSearchModal = $('#advanced-search-modal');
                $('.open-modal-advanced-search').click(function () {
                    advancedSearchModal.modal('show');
                });
                advancedSearchModal.on('show.bs.modal', function (e) {
                    setTimeout(function () {
                        var map = new google.maps.Map(document.getElementById('search-modal-map'), {
                            center: {lat: -34.397, lng: 150.644},
                            scrollwheel: false,
                            zoom: 8
                        });
                        new google.maps.Marker({
                            map: map,
                            position: {lat: -34.197, lng: 150.844}
                        });
                        new google.maps.Marker({
                            map: map,
                            position: {lat: -34.308, lng: 150.679},
                        });
                        new google.maps.Marker({
                            map: map,
                            position: {lat: -34.390, lng: 150.664}
                        });
                        new google.maps.Circle({
                            map: map,
                            center: {lat: -34.397, lng: 150.644},
                            radius: 100000,    // 10 miles in metres
                            fillColor: '#eed5a9',
                            fillOpacity: 0.3,
                            strokeColor: '#40b2cd',
                            strokeOpacity: 1,
                            strokeWeight: 3
                        });
                    }, 300)
                });
            });

        }, 500);
        
    }
}