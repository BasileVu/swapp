import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-your-inventory]' })
export class YourInventoryDirective {

    @Input('update-your-inventory')
    set updateYourInventory(update : boolean){
        if(update) {
            setTimeout(function(){
                $('.swapp-inventory-yours').flickity({
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
            }, 300);

        }
    }
}