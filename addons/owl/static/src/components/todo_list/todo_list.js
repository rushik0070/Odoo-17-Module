/** @odoo-module **/

import {registry} from  '@web/core/registry';
const {Component, useState, onWillStart, useRef} = owl;
import { useService } from "@web/core/utils/hooks";

export class OwlTodoList extends Component{
    setup(){
        this.state = useState({
            task:{name:"", description:"", completed:false},
            taskList:[],
            isEdit: false,
            activeId: false,
            // taskList:[1,2,3]
            // isClearButtonvisible: false,
        })
        this.orm = useService("orm")
        this.model = "todo.list"
        this.searchInput = useRef("search-input")
        this.filters = useRef("filters")

        onWillStart(async()=>{
            await this.getalltask()
        })
    }

    async filter(event){
        const filters = event.target.getAttribute("value");
        console.log("filter get ----" + filters);
        if (filters === 'all'){
            console.log(" if is working ---- ")
            this.state.taskList = await this.orm.searchRead(this.model , [], ["name","description","completed"])        
        }
        else{
            this.state.taskList = await this.orm.searchRead(this.model , [['description' , 'ilike' , filters]], ["name","description","completed"])
        }
    
    }

    async getalltask(){
        this.state.taskList = await this.orm.searchRead(this.model,[],["name","description","completed"])
    }

    async searchtask(){
        const text = this.searchInput.el.value
        console.log("search text get --- " + text)
        this.state.taskList = await this.orm.searchRead(this.model , [['name' , 'ilike' , text]] , ["name","description","completed"])
    }

    addTask(){
                this.resetform()
                this.state.isEdit = false
                this.state.activeId = false
                this.saveTask()
    }

    editTask(task){
        console.log("Edit Task Function IS Called",task)
        this.state.activeId = task.id
        this.state.isEdit = true
        this.state.task = {name:task.name,description:task.description,completed:task.completed}
    }

    async saveTask(){
        if (this.state.isEdit){
            console.log("write method is call for --- : " + this.state.task.name)
            await this.orm.write(this.model,  [this.state.activeId] , this.state.task)
        }else{
            console.log("create method is call")
            await this.orm.create(this.model, [this.state.task])
        }
        await this.getalltask()
    }

    resetform(){
        this.state.task = {name:"", description:"", completed:false}
    }

    async deletetask(task){
        console.log("Delete Task Function IS Called ---  :" + task)
        await this.orm.unlink(this.model, [task.id])
        await this.getalltask()
    }
}

OwlTodoList.template = 'owl.TodoList'
registry.category('actions').add('owl.action_todo_list_js',OwlTodoList);