$('document').ready(function() {
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
});