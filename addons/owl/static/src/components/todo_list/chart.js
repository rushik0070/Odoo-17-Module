/** @odoo-module **/

import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef, onMounted } = owl;
import { useService } from "@web/core/utils/hooks";
import {jsonrpc} from '@web/core/network/rpc_service';
// import { Chart } from 'chart.js';


export class OWlChartJS extends Component {
    setup() {
        this.action = useService("action");
        console.log("Action service initialized:", this.action);
        this.redirectToForm = this.redirectToForm.bind(this);
        this.state = useState({
            sum : {
                total_sale:0,
                total_sale_ids : [],
                total_sale_quotation:0,
                total_sale_quotation_ids:[],
                total_sale_order:0,
                total_sale_order_ids:[]
            },
            sales_ids : [],
            sale_data : [],
            visibleChart: null,
            current_type : 'doughnut',
            current_filter : 'gross',
            current_group_by : ''
        });
        console.log("&&&&&&&&&&&&&&&&&&&&&&&&",this.state.total_sale_ids)
        console.log("&&&&&&&&&&&&&&&&&&&&&&&&",this.state.total_sale_quotation_ids)
        console.log("&&&&&&&&&&&&&&&&&&&&&&&&",this.state.total_sale_order_ids)

        this.orm = useService("orm");
        this.model = "sale.order";
        this.doughnut_chart = useRef('sales_chart_doughnut');
       
        onWillStart(async()=>{
            await this.get_total(),
            await this.get_sales_data()
        })
        onMounted(async()=>{
            console.log("Component Mounted:", this.el);
            await this.render_sales_price()
        })
    }
    
    async get_sales_data() {
        this.state.sale_data = await this.orm.searchRead(this.model,[],["id","name","amount_total"])
    }

    async redirectToForm(recordId) {
        console.log("## Redirecting to Form ##", recordId);
    
        if (this.action) {
            this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "sale.order",
                res_id: recordId,
                views: [[false, "form"]],
                target: "current",
            });
        } else {
            console.error("Action service is not available.");
        }
    }
    
    async get_total(){
        try {
            const countdata = await jsonrpc("/get/sale/data", {});
            console.log("---- get total ---- ", countdata);
            console.log("---- get total 11---- ", countdata.total_order_ids);
            console.log("---- get total 22---- ", countdata.total_sale_quotation_ids);
            console.log("---- get total 33---- ", countdata.total_sale_order_ids);


            this.state.sum.total_sale = countdata.total_order;
            this.state.sum.total_sale_ids = countdata.total_order_ids,
            this.state.sum.total_sale_quotation = countdata.total_quotation;
            this.state.sum.total_sale_quotation_ids = countdata.total_sale_quotation_ids;
            this.state.sum.total_sale_order = countdata.total_sale_order;
            this.state.sum.total_sale_order_ids = countdata.total_sale_order_ids;
            this.state.sales_ids = countdata.order_ids;

            console.log("---- get total 111---- ", this.state.sum.total_sale_ids);
            console.log("---- get total 222---- ", this.state.sum.total_sale_quotation_ids);
            console.log("---- get total 333---- ", this.state.sum.total_sale_order_ids);
        } catch (error) {
            console.error("Failed to fetch total sales data:", error);
        }

        // jsonrpc("/get/sale/data",{}).then(function(data_dict){
        //     self.state.sum.total_sale = data_dict.total_order
        //     self.state.sales_ids = data_dict.order_ids
        // })
    }

    
    async get_sale_data(){
        console.log("get sale data is caelled ")
        const saleData = await jsonrpc("/get/sale/data", {});
        return saleData
    }

    async get_chart_values(filterType,chart_type){
        let order_name = []; // This will hold the customer names
        let data = []; // This will hold the customer Data 
        const saleData = await this.get_sale_data()
        const current_group = this.state.current_group_by
        order_name = saleData.order_name || [];
        let customer_name = saleData.customer_name || [];

        if (chart_type == 'doughnut'){
            if (filterType === 'gross'){
                data = saleData.net_amount || [];
            }
            else if(filterType === 'tax'){
                data = saleData.tax_amount || [];
            }
            else{
                data = saleData.untaxed || [];
            }
        }
        else{
            
            if (filterType === 'gross'){
                data = saleData.net_amount || [];
            }
            else if(filterType === 'tax'){
                data = saleData.tax_amount || [];
            }
            else{
                data = saleData.untaxed || [];
            }
            if (current_group == 'group_by_month'){
                let empty_order = []
                order_name = empty_order
                
                saleData.group_by_customer.forEach(customerData => {
                    let customer_name = Object.keys(customerData)[0];
                    order_name.push(customer_name)

                    let customer_values = customerData[customer_name]; 

                    let dataforcustomer = {
                        untaxed : customer_values.amount_untaxed,
                        tax_amount: customer_values.amount_tax,
                        net_amount: customer_values.amount_total
                    }
                    if(chart_type == 'gross'){
                        data.push(dataforcustomer.net_amount)
                    }
                    else if(chart_type == 'tax'){
                        data.push(dataforcustomer.amount_tax)
                    }
                    else{
                        data.push(dataforcustomer.amount_untaxed)
                    }
                });
            }
        }

        return{
            labels: order_name,
            datasets: [{
                label: filterType || '' + ' Sale Order Price',
                data: data, 
                backgroundColor: [
                  'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1,
                hoverOffset: 4
              }]
        }
    }
    async create_chart(filterType,chart_type){

        const chartdata = await this.get_chart_values(filterType,chart_type);
        const chartContainer1 = this.doughnut_chart.el;
        if (!chartContainer1) { 
            console.error("Sales chart container not found!");
            return;
        }
        
        const ctx = chartContainer1.getContext('2d');

        if(this.chartInstance){
            console.log("Destroying existing chart");
            this.chartInstance.destroy();
        }
        if (chart_type == 'doughnut'){
            if(ctx){
                console.log("ctx is finding ------ ",ctx)
                this.chartInstance = new Chart(ctx,{
                    type: 'doughnut',
                    data: chartdata,
                })
            }
        }
        else{
            this.chartInstance = new Chart(ctx,{
                type: 'bar',
                data: chartdata,
            })
        }
    }

    async render_sales_price(){
        console.log("render first time is called")
        const filterType = this.state.current_filter
        console.log("first time filter $",filterType)
        const chart_type = this.state.current_type
        console.log("first time chart_type $",chart_type)
        const group_by = this.state.current_group_by
        console.log("first time group_by $",group_by)

        await this.create_chart(filterType,chart_type,group_by);
    }

    on_click_sales(){
        console.log("$$ all sales order is show $$")
        var sales_ids = this.state.sales_ids
        var options = {
            additional : {},
            ClearBreadcrumbs:true
        }

        let xml_id = "sale.action_quotations_with_onboarding"
        let context = {}
        if(sales_ids){
            this.action.doAction(xml_id,{
                options
            })
        }
    }

    on_click_sales_quotation(){
        console.log("$$ Quotation sales order is show $$")
        var sales_ids = this.state.sum.total_sale_quotation_ids
        console.log("$$ total_sale_quotation_ids $$",sales_ids)
        console.log("Component is loaded:", );
        var options = {
            additional : {},
            ClearBreadcrumbs:true,
            context : {'search_default_draft': 1}
        }

        let xml_id = "sale.action_quotations_with_onboarding"
        let context = {}
        if(sales_ids){
            this.action.doAction(xml_id,{
                options
            })
        }
    }

    on_click_sales_order(){
        console.log("$$ Done sales order is show $$")
        var sales_ids = this.state.sum.total_sale_order_ids
        console.log("$$ total_sale_order_ids $$",sales_ids)
        var options = {
            additional : {},
            ClearBreadcrumbs:true,
            context : {'search_default_sales': 1}
        }

        let xml_id = "sale.action_quotations_with_onboarding"
        let context = {'search_default_sales': 1}
        if(sales_ids){
            this.action.doAction(xml_id,{
                additional_context : {
                options
                }
            })
        }
    }

    on_click_gross_chart(event){
        const chart_type = this.state.current_type
        const filterType = event.target.getAttribute("value");
        console.log("-- drop down --",filterType)
        if (chart_type == 'doughnut'){
            this.create_chart(filterType,chart_type)
        }
        else{
            this.create_chart(filterType,chart_type)
        }
    }

    on_click_tax_chart(event) {
        const chart_type = this.state.current_type
        const filterType = event.target.getAttribute("value");
        console.log("-- drop down --",filterType)
        if (chart_type == 'doughnut'){
            this.create_chart(filterType,chart_type)
        }
        else{
            this.create_chart(filterType,chart_type)
        }
    }

    on_click_net_chart(event) {
        const chart_type = this.state.current_type
        const filterType = event.target.getAttribute("value");
        console.log("-- drop down --",filterType)
        if (chart_type == 'doughnut'){
            this.create_chart(filterType,chart_type)
        }
        else{
            this.create_chart(filterType,chart_type)
        }

    }

    on_click_doughnut_chart(event) {
        const chart_type = event.target.getAttribute("value");
        const filterType = this.state.current_filter
        console.log("-- Chart Type --",chart_type)
        this.create_chart(filterType,chart_type)
        this.state.current_type = 'doughnut'

    }

    on_click_bar_chart(event) {
        const chart_type = event.target.getAttribute("value");
        const filterType = this.state.current_filter
        console.log("-- Chart Type --",chart_type)
        this.create_chart(filterType,chart_type)
        this.state.current_type = 'bar'
    }

    on_click_group_by_month(event) {
        const group_by = event.target.getAttribute("value");
        console.log("-- group_by --",group_by)
        this.create_chart()
        this.state.current_group_by = group_by
    }

    on_click_group_by_customer(event) {
        const group_by = event.target.getAttribute("value");
        console.log("-- group_by --",group_by)
        this.create_chart()
        this.state.current_group_by = group_by

    }
}

console.log("Component is loaded:", OWlChartJS);
OWlChartJS.template = 'owl.ChartJs';
registry.category('actions').add('owl.action_chart_js', OWlChartJS);
