/** @odoo-module **/

import {registry} from "@web/core/registry";
import {SystrayLauncherButton} from "@traction/components/common";

export class SystrayIssues extends SystrayLauncherButton{
    setup() {
        this.actionName = "traction_issue_view_form_simple_modif";
        this.actionDialogTitle = "Raise Issue";
        this.model = "traction.issue";
        this.modelDisplayName = "Issue";
        super.setup(...arguments);
    }
}

SystrayIssues.template = "traction.SystrayIssues"

export const systrayItem = {
    Component: SystrayIssues,
};

registry.category(
    "systray").add(
    "traction.SystrayIssues",
    systrayItem, {
        sequence: 1000
    }
);