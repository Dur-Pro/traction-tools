odoo.define('traction.Dashboard', function (require){
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core')

var TractionDashboard = AbstractAction.extend({
    template: 'TractionDashboard',
});

core.action_registry.add('traction_dashboard', TractionDashboard);

return TractionDashboard;

});