import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-carousel]' })
export class UpdateCarouselDirective {

    @Input('update-carousel')
    set updateBigPicture(update : boolean){
        if(update) {
            // $('.modal-carousel').flickity('destroy');

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
        }
    }
}