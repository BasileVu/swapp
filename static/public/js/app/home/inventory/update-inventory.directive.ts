import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-inventory]' })
export class UpdateInventoryDirective {

    @Input('update-inventory')
    set updateInventory(update : boolean){
        if(update) {
            // modal slider ///////////////////////////
            let modalCarousel = $('.modal-carousel-inventory').flickity({
                cellAlign: 'center',
                contain: true,
                imagesLoaded: true,
                wrapAround: true,
                prevNextButtons: false,
                adaptiveHeight: true
            });

            let flkty = modalCarousel.data('flickity');
        }
    }
}