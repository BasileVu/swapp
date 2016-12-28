"use strict";
var core_1 = require('@angular/core');
var ToastOptions = (function () {
    function ToastOptions(options) {
        this.newestOnTop = false;
        this.animate = 'fade';
        this.enableHTML = false;
        this.showCloseButton = false;
        Object.assign(this, options);
    }
    ToastOptions.decorators = [
        { type: core_1.Injectable },
    ];
    /** @nocollapse */
    ToastOptions.ctorParameters = [
        { type: Object, },
    ];
    return ToastOptions;
}());
exports.ToastOptions = ToastOptions;
//# sourceMappingURL=toast-options.js.map