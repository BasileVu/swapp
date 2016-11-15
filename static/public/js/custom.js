$('document').ready(function() {
    // home grid ///////////////////////////
    var $grid = $('.grid').isotope({
        // options
        itemSelector: '.grid-item',
        layoutMode: 'masonry'
    });
    $grid.imagesLoaded().progress( function() {
        $grid.isotope('layout');
    });

    $('.grid-item').hover(function () {
        $(this).addClass('hovered');
        $grid.isotope('layout');
    }, function () {
        $(this).removeClass('hovered');
        $grid.isotope('layout');
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
    var $carousel = $('.modal-carousel').flickity({
        cellAlign: 'center',
        contain: true,
        imagesLoaded: true,
        wrapAround: true,
        prevNextButtons: false,
        adaptiveHeight: true
    });

    var $carouselNav = $('.modal-carousel-nav');
    var $carouselNavCells = $carouselNav.find('.carousel-cell');

    $carouselNav.on( 'click', '.carousel-cell', function( event ) {
        var index = $( event.currentTarget ).index();
        $carousel.flickity( 'select', index );
    });

    var flkty = $carousel.data('flickity');
    var navCellHeight = $carouselNavCells.height();
    var navHeight = $carouselNav.height();

    $carousel.on( 'select.flickity', function() {
        // set selected nav cell
        $carouselNav.find('.is-nav-selected').removeClass('is-nav-selected');
        var $selected = $carouselNavCells.eq( flkty.selectedIndex )
            .addClass('is-nav-selected');
        // scroll nav
        var scrollY = $selected.position().top +
            $carouselNav.scrollTop() - ( navHeight + navCellHeight ) / 2;
        $carouselNav.animate({
            scrollTop: scrollY
        });
    });

    // display modal ///////////////////////////
    $('#view-item-x').on('show.bs.modal', function (e) {
        setTimeout(function () {
            $('.modal-carousel').flickity('resize');
            $('.modal-carousel-height').matchHeight({
                byRow: false,
                target: $('.modal-carousel')
            });
        }, 300)
    });
    $('.open-modal-item-x').click(function () {
        $('#view-item-x').modal('show');
    });
});