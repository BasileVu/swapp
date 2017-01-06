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

                /*
                 TODO : remove because it's handled in items/*.directive.ts
                // home grid ///////////////////////////
                let grid = $('.grid').isotope({
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
                */

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

                // display item modal ///////////////////////////
                let theItemModal = $('#view-item-x');
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

                // advanced search ///////////////////////////
                let advancedSearchModal = $('#advanced-search-modal');
                $('.open-modal-advanced-search').click(function () {
                    advancedSearchModal.modal('show');
                });
                advancedSearchModal.on('show.bs.modal', function (e) {
                    setTimeout(function () {
                        let map = new google.maps.Map(document.getElementById('search-modal-map'), {
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