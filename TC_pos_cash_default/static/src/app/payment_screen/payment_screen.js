/** @odoo-module **/
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Order.prototype, {

    setup() {
        super.setup(...arguments);
    },
    async pay(){
        super.pay()
        // Check if a cash payment method exists
        const cashPaymentMethod = this.pos.payment_methods.find(method => method.id === this.pos.config.default_cash_method[0]);
        if (cashPaymentMethod) {
          // Check if there are any existing payment lines
            const hasOtherPaymentLines = this.paymentlines.length > 0;
            if (!hasOtherPaymentLines) {
            // No other payment lines exist, add the cash payment line
            this.add_paymentline(cashPaymentMethod);
            } else {
            // If there are other payment lines, check if cash is already selected
                const existingPaymentLine = this.paymentlines.find(line => line.payment_method.id === cashPaymentMethod.id);
                if (!existingPaymentLine) {
                    // Cash is not selected; you can decide how to handle this case
                    this.select_paymentline(existingPaymentLine || this.paymentlines[0]); // Select the first payment line if cash isn't present
                }
            }
        }
    },
});