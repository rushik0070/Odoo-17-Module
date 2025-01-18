/** @odoo-module **/

import {registry} from  '@web/core/registry';
const {Component, useState, onWillStart, useRef} = owl;
import { useService } from "@web/core/utils/hooks";
import {jsonrpc} from '@web/core/network/rpc_service';
import { _t } from "@web/core/l10n/translation";


export class Task extends Component{
    setup(){
        this.notificationService = useService("notification");
        this.state = useState({
            task_data : [],
            employee : [],
            task_name : '',
            task_start_time : '',
            task_end_time : '',
            task_manager : '',
            task_priority : '1'
        
        });

        onWillStart(async()=>{
            await this.get_task_data()
            await this.get_employee_name()
        })
    }

    async get_task_data(){
        try{
            let task_data = await jsonrpc("/get/task/data",{});
            console.info("$$$ task data $$$",task_data)
            this.state.task_data = task_data;
            console.log("TASK DATA ---->>>",this.state.task_data)
        }
        catch(error){
            console.error("Failed to fetch task data:", error);
        }
    }

    async get_employee_name(){
        console.log("$$ user click in this funxtion $$")
        try{
            let employee_data = await jsonrpc("/get/employee/name",{});
            console.log("$$$ employee data $$$",employee_data)
            this.state.employee = employee_data;
            console.log("state user data",this.state.employee)
        }
        catch(error){
            console.error("Failed to fetch Employee data:", error);
        }
    }

    save_data(){
        console.log("$$$ user click in save data function $$$");
        console.log("Current task manager:", this.state.task_manager);
        const taskData = {
            name: this.state.task_name,
            manager_id: this.state.task_manager,
            start_date: this.state.task_start_time,
            end_date: this.state.task_end_time,
            priority: this.state.task_priority,
        };
        console.log(" ---------->>>> getting form data $$",taskData)

        let missign_record = []
        // if (!taskData.name)missign_record.push()
        if(taskData.name == '' || taskData.manager_id == '' || taskData.start_date == '' || taskData.end_date == ''){
            const message = 'Missing Record'
            const type = 'danger'
            const title = 'Error'
            this._notify(message,type,title)
        }
    }

    _notify(message,type){
        this.notificationService.add(_t(message),{
            title : title,
            type : type
        });
    }

}

Task.template = 'owl.Task'
registry.category('actions').add('owl.action_task_js',Task);