import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-inventory]' })
export class UpdateInventoryDirective {

    @Input('update-inventory')
    set updateInventory(update : boolean){
        if(update) {
            // home inventory /////// ////////////////////
            $('.home-inventory').flickity({
                // options
                cellAlign: 'center',
                contain: true,
                imagesLoaded: true,
                wrapAround: true,
                groupCells: '100%',
                prevNextButtons: false,
                adaptiveHeight: true
            });

            // open item creation modal /////////////////////
            $('.open-new-item-modal').each(function () {
                $(this).click(function () {
                    $('#add-item-modal').modal('show');
                });
            });
            $('.open-modal-item-x').click(function () {
                $('#view-item-x').modal('show');
            });
        }
    }
}