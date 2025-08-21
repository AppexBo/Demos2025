/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.observadorPOS(this.pos);
	}, 

    observadorPOS(pos){
        const observer = new MutationObserver(() => {
            this.hide_in_information_finanzas();
            this.hide_in_information_ordenars();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    hide_in_information_finanzas(){
        const section_financials = document.querySelectorAll(".section-financials.mt-3.mb-4.pb-4.border-bottom.text-start");
        section_financials.forEach(section_financial => {
            const have_styles = section_financial.hasAttribute('style');
            if (!have_styles) {
                section_financial.setAttribute('style', 'display: none !important;')
            }
        });
    },

    hide_in_information_ordenars(){
        const section_orders = document.querySelectorAll(".section-order.mt-3.mb-4.pb-4.border-bottom.text-start");
        section_orders.forEach(section_order => {
            const have_styles = section_order.hasAttribute('style');
            if (!have_styles) {
                section_order.setAttribute('style', 'display: none !important;')
            }
        });
    },

});