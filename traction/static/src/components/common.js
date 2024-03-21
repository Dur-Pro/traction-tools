/** @odoo-module **/

import {useService, useBus} from "@web/core/utils/hooks";

import {Component, onWillStart} from "@odoo/owl";

export class SystrayLauncherButton extends Component {
    // This class is meant to be extended for a concrete implementation.
    setup() {
        if (!this.actionName || !this.actionDialogTitle || !this.model || !this.modelDisplayName) {
            throw new Error("Required paramaters are not set for SystrayLauncherButton!");
        }
        this.actionService = useService("action")
        this.orm = useService("orm")
        this.notification = useService("notification")
        useBus(this.env.bus, "ACTION_MANAGER:UPDATE", (payload) => {
            this.resModel = "resModel" in payload.detail.componentProps ? payload.detail.componentProps.resModel : false;
            this.resId = "resId" in payload.detail.componentProps ? payload.detail.componentProps.resId : false;
        })
        onWillStart(async () => {
            let action_data = await this.orm.searchRead(
                "ir.model.data",
                [["module", "=", "traction"], ["name", "=", this.actionName]],
                ["res_id"]);
            this.create_action_id = action_data[0]["res_id"]
        })
    }

    onClick() {
        let context = {}
        let self = this;
        if (this.resModel && this.resId) {
            context['res_model'] = this.resModel;
            context['res_id'] = this.resId;
        }
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: this.actionDialogTitle,
            res_model: this.model,
            target: "new",
            views: [
                [this.create_action_id, "form"],
            ],
            context: context,
        });
    }
}
