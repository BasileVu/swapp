"use strict";
var Image = (function () {
    function Image() {
    }
    return Image;
}());
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
        this.price_min = -1;
        this.price_max = -1;
        this.creation_date = new Date();
        this.archived = false;
        this.owner = { id: -1, profile_picture: "undef", location: "undef" };
        this.category = { id: -1, name: "undef" };
    }
    Item.prototype.getId = function () {
        return this.id;
    };
    return Item;
}());
exports.Item = Item;
//# sourceMappingURL=item.js.map