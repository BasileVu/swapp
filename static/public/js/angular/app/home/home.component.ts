import {Component, ViewEncapsulation, ViewChild, ElementRef, AfterViewInit,} from '@angular/core';

/* To use our JS library */
declare var $:jQueryStatic;

@Component({
    moduleId: module.id,
    selector: 'home',
    encapsulation: ViewEncapsulation.None,
    templateUrl: './home.component.html'
})

export class HomeComponent implements AfterViewInit {

    @ViewChild('grid') el:ElementRef;

    constructor() {
    }

    ngAfterViewInit() {
        var grid = $(this.el.nativeElement);
        grid.isotope({
            // options
            itemSelector: '.grid-item',
            layoutMode: 'masonry'
        });

        grid.imagesLoaded().progress( function() {
            grid.isotope('layout');
        });

        $('.grid-item').hover(function () {
            $(this).addClass('hovered');
            grid.isotope('layout');
        }, function () {
            $(this).removeClass('hovered');
            grid.isotope('layout');
        });
    }
}
