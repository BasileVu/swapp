"use strict";
var Owner = (function () {
    function Owner() {
        this.id = -1;
        this.first_name = "undef";
        this.last_name = "undef";
        this.username = "undef";
        this.profile_picture_url = "undef";
        this.inventory = new Array();
        this.score = 0;
        this.number_of_vote = 0;
        this.interested_in = new Array();
        this.delivery_address = "undef";
        this.delivery_methods = new Array();
    }
    return Owner;
}());
exports.Owner = Owner;
//# sourceMappingURL=owner.js.map