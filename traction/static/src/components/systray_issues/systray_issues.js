/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {session} from "@web/session";

const {Component} = owl;

export class SystrayIssues extends Component {
    setup() {
        this.actionService = useService("action");
    }

    onClick() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Raise Issue",
            res_model: "traction.issue",
            target: "new",
            views: [
                [false, "form"],
            ],
        });
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