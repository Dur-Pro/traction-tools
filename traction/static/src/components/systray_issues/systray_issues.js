/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {session} from "@web/session";
const {Component} = owl;

export class SystrayIssues extends Component {
    async setup() {
        this.actionService = useService("action");
        this.orm = useService("orm")
        let action_data = await this.orm.searchRead(
            "ir.model.data",
            [["module", "=", "traction"], ["name", "=", "traction_issue_view_form_simple_modif"]],
            ["res_id"]);
        this.create_action_id = action_data[0]["res_id"]
    }

    async onClick(ev) {
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Raise Issue",
            res_model: "traction.issue",
            target: "new",
            views: [
                [this.create_action_id, "form"],
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