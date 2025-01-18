/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class TaskManagerRedirect extends Component {
    /**
     * This function is triggered when the field is clicked.
     * It redirects to the related user's form view.
     */
    // onRedirect(event) {
    //     event.stopPropagation();
    //     const recordId = this.props.record.data.task_manager?.res_id;

    //     if (recordId) {
    //         this.env.services.action.doAction({
    //             type: "ir.actions.act_window",
    //             res_model: "res.users",
    //             res_id: recordId,
    //             views: [[false, "form"]],
    //         });
    //     }
    // }

    /**
     * Renders the many2one field value as a clickable link.
     */
    // get displayText() {
    //     return this.props.record.data.task_manager?.display_name || "";
    // }
}

TaskManagerRedirect.template = "owl.TaskManagerRedirect";

// Register the widget in the field registry
// registry.category("fields").add("task_manager_redirect", TaskManagerRedirect);

export default TaskManagerRedirect;