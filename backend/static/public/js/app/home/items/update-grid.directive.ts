import { Directive, Input } from '@angular/core';

declare let $:any;

@Directive({ selector: '[update-grid]' })
export class UpdateGridDirective {

    @Input('update-grid')
    set updateGrid(update : boolean){
        if(update) {
            setTimeout(function() {
                // $('.grid').isotope('destroy');
                $('.grid').isotope('reloadItems')

                $('.grid').isotope({
                    // options
                    itemSelector: '.grid-item',
                    layoutMode: 'masonry'
                });
                // layout only when images are loaded
                $('.grid').imagesLoaded().progress( function() {
                    $('.grid').isotope('layout');
                });
                // display items details when hovered
                $('.grid-item').hover(function () {
                    $(this).addClass('hovered');
                    $('.grid').isotope('layout');
                }, function () {
                    $(this).removeClass('hovered');
                    $('.grid').isotope('layout');
                });

                $('.open-modal-item-x').click(function () {
                    $('#view-item-x').modal('show');
                });
            }, 0);

        }
    }
}