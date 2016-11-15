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
    var theModal = $('#view-item-x');
    // show.bs.modal would be better, but not working in bootstrap 4 alpha 4
    theModal.on('show.bs.modal', function (e) {
        setTimeout(function () {
            modalCarousel.flickity('resize');
            $('.modal-carousel-height').matchHeight({
                byRow: false,
                target: modalCarousel
            });
        }, 300)
    });
    $('.open-modal-item-x').click(function () {
        theModal.modal('show');
    });
});