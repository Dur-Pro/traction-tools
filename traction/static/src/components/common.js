/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService, useBus} from "@web/core/utils/hooks";

const {Component} = owl;
const {onWillStart} = owl.hooks;

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
            this.resModel = "resModel" in payload.componentProps ? payload.componentProps.resModel : false;
            this.resId = "resId" in payload.componentProps ? payload.componentProps.resId : false;
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
        }, {
            onClose: (onCloseInfo) => {
                if (onCloseInfo && "special" in onCloseInfo) {
                    // The cancel button was pressed, do nothing
                    return;
                } else {
                    this.notification.add(
                        `${this.modelDisplayName} successfully created.`,
                        {type: "success"},
                    )
                }
            }
        });
    }
}
