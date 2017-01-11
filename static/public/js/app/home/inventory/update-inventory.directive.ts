import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-inventory]' })
export class UpdateInventoryDirective {

    @Input('update-inventory')
    set updateInventory(update : boolean){
        if(update) {

            setTimeout(function(){

                // modal slider ///////////////////////////
                let modalCarousel = $('.modal-carousel-inventory').flickity({
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    prevNextButtons: false,
                    adaptiveHeight: true
                });

                //let flkty = modalCarousel.data('flickity');



                let modalCarouselNav = $('.modal-carousel-nav');
                let modalCarouselNavCells = modalCarouselNav.find('.carousel-cell');

                modalCarouselNav.on( 'click', '.carousel-cell', function( event: any ) {
                    let index = $( event.currentTarget ).index();
                    modalCarousel.flickity( 'select', index );
                });

                let flkty = modalCarousel.data('flickity');
                let navCellHeight = modalCarouselNavCells.height();
                let navHeight = modalCarouselNav.height();

                modalCarousel.on( 'select.flickity', function() {
                    // set selected nav cell
                    modalCarouselNav.find('.is-nav-selected').removeClass('is-nav-selected');
                    let selected = modalCarouselNavCells.eq( flkty.selectedIndex )
                        .addClass('is-nav-selected');
                    // scroll nav
                    let scrollY = selected.position().top +
                        modalCarouselNav.scrollTop() - ( navHeight + navCellHeight ) / 2;
                    modalCarouselNav.animate({
                        scrollTop: scrollY
                    });
                });


            }, 300);



            /*
            setTimeout(function(){

                // modal slider ///////////////////////////
                let modalCarousel = $('.modal-carousel').flickity({
                    cellAlign: 'center',
                    contain: true,
                    imagesLoaded: true,
                    wrapAround: true,
                    prevNextButtons: false,
                    adaptiveHeight: true
                });

                let modalCarouselNav = $('.modal-carousel-nav');
                let modalCarouselNavCells = modalCarouselNav.find('.carousel-cell');

                modalCarouselNav.on( 'click', '.carousel-cell', function( event: any ) {
                    let index = $( event.currentTarget ).index();
                    modalCarousel.flickity( 'select', index );
                });

                let flkty = modalCarousel.data('flickity');
                let navCellHeight = modalCarouselNavCells.height();
                let navHeight = modalCarouselNav.height();

                modalCarousel.on( 'select.flickity', function() {
                    // set selected nav cell
                    modalCarouselNav.find('.is-nav-selected').removeClass('is-nav-selected');
                    let selected = modalCarouselNavCells.eq( flkty.selectedIndex )
                        .addClass('is-nav-selected');
                    // scroll nav
                    let scrollY = selected.position().top +
                        modalCarouselNav.scrollTop() - ( navHeight + navCellHeight ) / 2;
                    modalCarouselNav.animate({
                        scrollTop: scrollY
                    });
                });

            }, 300);
            */
        }
    }
}