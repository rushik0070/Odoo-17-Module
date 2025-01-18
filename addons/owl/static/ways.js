/** @odoo-module **/

import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef, onMounted } = owl;
import { useService } from "@web/core/utils/hooks";
import {jsonrpc} from '@web/core/network/rpc_service';
// import { Chart } from 'chart.js';


export class OWlChartJS extends Component {
    setup() {
        this.action = useService("action");
        this.state = useState({
            sum : {
                total_sale:0,
                total_sale_quotation:0,
                total_sale_order:0
            },
            sales_ids : []
        });
        this.orm = useService("orm");
        this.model = "sale.order";

        // this.chartRef = useRef('sales_chart');
        this.chartRef = useRef('sales_chart');

        // ####### 1st Way Fetch Count From OWL #############

        onWillStart(async()=>{
            await this.get_total()
        })
        onMounted(async()=>{
            console.log("Component Mounted:", this.el);
            await this.render_sales_price()
        })

        // ####### 2nd Way Fetch Count From Controller #############

        // onWillStart(this.onWillStart);
    }

    // ####### 1st Way Fetch Count From OWL #############

    // async get_total() {
    //    console.log("function is called")
    //    const result = await this.orm.searchRead(this.model,[],["name"])
    //    this.state.sum.total_sale = result.length

    //    const result2 = await this.orm.searchRead(this.model,[['state','=','draft']],["name"])
    //    this.state.sum.total_sale_quotation = result2.length

    //    const result3 = await this.orm.searchRead(this.model,[['state','=','sale']],["name"])
    //    this.state.sum.total_sale_order = result3.length
    // }

    // ####### 2nd Way Fetch Count From Controller #############

    // async onWillStart(){
    //     await this.get_total()
    // }

    async get_total(){
        var self = this;
        jsonrpc("/get/sale/data",{}).then(function(data_dict){
            self.state.sum.total_sale = data_dict.total_order
            self.state.sales_ids = data_dict.order_ids
        })
    }

    async render_sales_price(){

        const chartContainer1 = this.chartRef.el;
        if (!chartContainer1) {
            console.error("Sales chart container not found!");
            return;
        }
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 400;
        chartContainer1.appendChild(canvas);
        console.log("--- chart function is called ---")
        var self = this;
        var data = {
            labels: [
                'Red',
                'Blue',
                'Yellow'
              ],
            datasets: [{
                label: 'My First Dataset',
                data: [300, 50, 100],
                backgroundColor: [
                  'rgb(255, 99, 132)',
                  'rgb(54, 162, 235)',
                  'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
              }]
        }
        // var ctx = $('.myChart')
        const ctx = canvas.getContext('2d');
        jsonrpc("/get/sale/data",{
            
        }).then(function(data_dict){

        })
        if(ctx){
            console.log("ctx is finding ------ ",ctx)
            new Chart(ctx,{
                type: 'doughnut',
                data: data,
            })
        }
        // var chart = new Chart(ctx,{
        //     type: 'doughnut',
        //     data : data

        // })
    }

    on_click_sales(){
        var sales_ids = this.state.sales_ids
        var options = {
            additional : {},
            ClearBreadcrumbs:true
        }
        // ################ Action Way 1 ##############################

        // if(sales_ids){
        //     console.log("onclick is working")
        //     this.action.doAction({
        //         name : ("Projects"),
        //         type : 'ir.actions.act_window',
        //         res_model : 'sale.order',
        //         view_mode : 'form',
        //         views : [[false,'list'],[false,'form']],
        //         domain : [['id','in',sales_ids]],
        //         context : {
        //             create : false
        //         },
        //         target : 'current'

        //     },options)
        // }

        // ################ Action Way 2 ##############################
        let xml_id = "sale.action_quotations_with_onboarding"
        let context = {}
        if(sales_ids){
            this.action.doAction(xml_id,{
                options
            })
        }

    }
}

console.log("Component is loaded:", OWlChartJS);
OWlChartJS.template = 'owl.ChartJs';
registry.category('actions').add('owl.action_chart_js', OWlChartJS);
