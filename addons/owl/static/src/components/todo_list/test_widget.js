/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class ShowCurrentTime extends Component{
    setup(){
        console.log("show_current_date_time is called")
    }
    showPopup(){
        console.log("show_current_date_time is called")
    }
}
ShowCurrentTime.template = 'owl.CurrentDate'
registry.category("view_widgets").add("show_current_date_time",ShowCurrentTime)