import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-my-inventory]' })
export class MyInventoryDirective {

    @Input('update-my-inventory')
    set updateMyInventory(update : boolean){
        if(update) {
            setTimeout(function(){
                // swapp inventories /////////////////////////
                $('.swapp-inventory-mine').flickity({
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