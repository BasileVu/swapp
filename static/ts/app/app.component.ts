import {Component, OnInit, AfterViewInit} from '@angular/core';

import './rxjs-operators';
import {Http} from "@angular/http";

declare var $:any;
declare var google: any;

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: 'app.component.html'
})
export class AppComponent implements OnInit, AfterViewInit {
    subtitle = '(v1)';

    constructor (private http: Http) {}

    ngOnInit() {
        this.http.get("/api/csrf/");
    }

    ngAfterViewInit() {

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
            $('#home-inventory').flickity({
                // options
                cellAlign: 'center',
                contain: true,
                imagesLoaded: true,
                wrapAround: true,
                groupCells: '100%',
                prevNextButtons: false,
                adaptiveHeight: true
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

            // display modal ///////////////////////////
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
                    var marker = new google.maps.Marker({
                        map: map,
                        position: {lat: -34.197, lng: 150.844}
                    });
                    var marker = new google.maps.Marker({
                        map: map,
                        position: {lat: -34.308, lng: 150.679},
                    });
                    var marker = new google.maps.Marker({
                        map: map,
                        position: {lat: -34.390, lng: 150.664}
                    });
                    var circle = new google.maps.Circle({
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

    }
}