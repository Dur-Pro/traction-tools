/** @odoo-module **/

import {registry} from "@web/core/registry";
import {SystrayLauncherButton} from "@traction/components/common";

export class SystrayHeadlines extends SystrayLauncherButton{
    setup() {
        this.actionName = "traction_headline_view_form_simple_modif";
        this.actionDialogTitle = "Add Headline";
        this.model = "traction.headline";
        this.modelDisplayName = "Headline";
        super.setup(...arguments);
    }
}

SystrayHeadlines.template = "traction.SystrayHeadlines"

export const systrayItem = {
    Component: SystrayHeadlines,
};

registry.category(
    "systray").add(
    "traction.SystrayHeadlines",
    systrayItem, {
        sequence: 1000
    }
);
