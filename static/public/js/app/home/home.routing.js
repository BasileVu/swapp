"use strict";
var router_1 = require('@angular/router');
var home_component_1 = require('./home.component');
// noinspection TypeScriptValidateTypes
var routes = [
    {
        path: '',
        component: home_component_1.HomeComponent,
        children: []
    }
];
exports.routing = router_1.RouterModule.forChild(routes);
//# sourceMappingURL=home.routing.js.map