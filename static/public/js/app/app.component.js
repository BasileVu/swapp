"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
require('./rxjs-operators');
var http_1 = require("@angular/http");
var authentication_service_1 = require('./shared/authentication/authentication.service');
var AppComponent = (function () {
    function AppComponent(http, authService) {
        this.http = http;
        this.authService = authService;
        this.subtitle = '(v1)';
    }
    AppComponent.prototype.ngOnInit = function () {
        var _this = this;
        var csrf = this.http.get("/api/csrf/");
        console.log(csrf);
        this.loggedIn = this.authService.isLoggedIn();
        // Listen for login changes
        this.subscription = this.authService.loggedInSelected$.subscribe(function (loggedIn) { return _this.loggedIn = loggedIn; });
        // TODO : make a proper service to store geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                localStorage.setItem("latitude", String(position.coords.latitude));
                localStorage.setItem("longitude", String(position.coords.longitude));
            });
        }
        else {
            console.log("Geolocation not available");
        }
    };
    AppComponent.prototype.ngAfterViewInit = function () {
        setTimeout(function () {
            $('document').ready(function () {
                // home grid ///////////////////////////
                var grid = $('.grid').isotope({
                    // options
                    itemSelector: '.grid-item',
                    layoutMode: 'masonry'
                });
                // layout only when images are loaded
                grid.imagesLoaded().progress(function () {
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
                modalCarouselNav.on('click', '.carousel-cell', function (event) {
                    var index = $(event.currentTarget).index();
                    modalCarousel.flickity('select', index);
                });
                var flkty = modalCarousel.data('flickity');
                var navCellHeight = modalCarouselNavCells.height();
                var navHeight = modalCarouselNav.height();
                modalCarousel.on('select.flickity', function () {
                    // set selected nav cell
                    modalCarouselNav.find('.is-nav-selected').removeClass('is-nav-selected');
                    var selected = modalCarouselNavCells.eq(flkty.selectedIndex)
                        .addClass('is-nav-selected');
                    // scroll nav
                    var scrollY = selected.position().top +
                        modalCarouselNav.scrollTop() - (navHeight + navCellHeight) / 2;
                    modalCarouselNav.animate({
                        scrollTop: scrollY
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
                    }, 300);
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
                    }, 300);
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
                            center: { lat: -34.397, lng: 150.644 },
                            scrollwheel: false,
                            zoom: 8
                        });
                        new google.maps.Marker({
                            map: map,
                            position: { lat: -34.197, lng: 150.844 }
                        });
                        new google.maps.Marker({
                            map: map,
                            position: { lat: -34.308, lng: 150.679 },
                        });
                        new google.maps.Marker({
                            map: map,
                            position: { lat: -34.390, lng: 150.664 }
                        });
                        new google.maps.Circle({
                            map: map,
                            center: { lat: -34.397, lng: 150.644 },
                            radius: 100000,
                            fillColor: '#eed5a9',
                            fillOpacity: 0.3,
                            strokeColor: '#40b2cd',
                            strokeOpacity: 1,
                            strokeWeight: 3
                        });
                    }, 300);
                });
            });
        }, 500);
    };
    AppComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'my-app',
            templateUrl: 'app.component.html',
            animations: [
                core_1.trigger('flyInOut', [
                    core_1.state('in', core_1.style({ opacity: 1, transform: 'translateX(0)' })),
                    core_1.transition('void => *', [
                        core_1.style({
                            opacity: 0,
                            transform: 'translateX(-100%)'
                        }),
                        core_1.animate('0.2s ease-in')
                    ]),
                    core_1.transition('* => void', [
                        core_1.animate('0.2s 10 ease-out', core_1.style({
                            opacity: 0,
                            transform: 'translateX(100%)'
                        }))
                    ])
                ])
            ]
        }), 
        __metadata('design:paramtypes', [http_1.Http, authentication_service_1.AuthService])
    ], AppComponent);
    return AppComponent;
}());
exports.AppComponent = AppComponent;
//# sourceMappingURL=app.component.js.map