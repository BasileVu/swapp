$('document').ready(function() {
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
    })
});