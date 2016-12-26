"use strict";
var Like = (function () {
    function Like() {
    }
    return Like;
}());
var Item = (function () {
    function Item() {
        this.id = -1;
        this.name = "undef";
        this.description = "undef";
        this.image_url = "undef";
        this.image_set = new Array();
        this.price_min = -1;
        this.price_max = -1;
        this.key_informations = new Array();
        this.creation_date = new Date();
        this.city = "undef";
        this.country = "undef";
        this.offers_received = 0;
        this.views = 0;
        this.likes = 0;
        this.comments = 0;
        this.owner = -1;
        this.owner_image_url = "undef";
        this.category = { id: -1, name: "undef" };
        this.similars = new Array();
    }
    Item.prototype.getId = function () {
        return this.id;
    };
    return Item;
}());
exports.Item = Item;
//# sourceMappingURL=item.js.map