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
    var inventory = $('.home-inventory').flickity({
        // options
        cellAlign: 'center',
        contain: true,
        imagesLoaded: true,
        wrapAround: true,
        groupCells: '100%',
        prevNextButtons: false,
        adaptiveHeight: true
    });

    // swapp inventories /////////////////////////
    var swapp_inventory_mine = $('.swapp-inventory-mine').flickity({
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
    var swapp_inventory_yours = $('.swapp-inventory-yours').flickity({
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

    // open item creation modal /////////////////////
    var addItemButtons = $('.open-new-item-modal');
    var newItemModal = $('#add-item-modal');
    addItemButtons.each(function () {
        $(this).click(function () {
            newItemModal.modal('show');
        });
    });

    // open user edition modal /////////////////////
    var openUpdateProfileButtons = $('.open-update-profile-modal');
    var updateProfileModal = $('#update-user-modal');
    openUpdateProfileButtons.each(function () {
        $(this).click(function () {
            updateProfileModal.modal('show');
        });
    });

    // open user profile modal /////////////////////
    var openProfileButtons = $('.open-profile-modal');
    var profileModal = $('#user-profile-modal');
    openProfileButtons.each(function () {
        $(this).click(function () {
            profileModal.modal('show');
        });
    });
    profileModal.on('show.bs.modal', function (e) {
        setTimeout(function () {
            inventory.flickity('resize');

            // profile map
            var map = new google.maps.Map(document.getElementById('profile-map'), {
                center: {lat: -34.197, lng: 150.844},
                scrollwheel: false,
                zoom: 8
            });
            var marker = new google.maps.Marker({
                map: map,
                position: {lat: -34.197, lng: 150.844}
            });
            var infowindow = new google.maps.InfoWindow({
                content: '<h3 class="map-title">Adresse complète</h3>'
            });
            infowindow.open(map, marker);
        }, 300)
    });

    // open notif modal /////////////////////
    var openNotifButtons = $('.open-notif-modal');
    var notifModal = $('#notification-modal');
    openNotifButtons.each(function () {
        $(this).click(function () {
            notifModal.modal('show');
        });
    });

    // open send proposition modal /////////////////////
    var openSendPropositionButtons = $('.open-send-proposition-modal');
    var sendPropositionModal = $('#send-proposition-modal');
    openSendPropositionButtons.each(function () {
        $(this).click(function () {
            sendPropositionModal.modal('show');
        });
    });
    sendPropositionModal.on('show.bs.modal', function (e) {
        setTimeout(function () {
            swapp_inventory_mine.flickity('resize');
            swapp_inventory_yours.flickity('resize');
        }, 300)
    });

    // open accept proposition modal /////////////////////
    var openAcceptPropositionButtons = $('.open-accept-proposition-modal');
    var acceptPropositionModal = $('#accept-proposition-modal');
    openAcceptPropositionButtons.each(function () {
        $(this).click(function () {
            acceptPropositionModal.modal('show');
        });
    });

    // display item modal ///////////////////////////
    var theItemModal = $('#view-item-x');
    // show.bs.modal would be better, but not working in bootstrap 4 alpha 4
    theItemModal.on('show.bs.modal', function (e) {
        setTimeout(function () {
            modalCarousel.flickity('resize');
            $('.modal-carousel-height').matchHeight({
                byRow: false,
                target: modalCarousel
            });
        }, 300)
    });
    $('.open-modal-item-x').click(function () {
        theItemModal.modal('show');
    });

    // advanced search ///////////////////////////
    var advancedSearchModal = $('#advanced-search-modal');
    $('.open-modal-advanced-search').click(function () {
        advancedSearchModal.modal('show');
    });
});