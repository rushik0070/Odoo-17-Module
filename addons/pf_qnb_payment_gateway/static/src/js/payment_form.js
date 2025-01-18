/** @odoo-module */
/* global Stripe */

import { _t } from '@web/core/l10n/translation';
import { QnbOptions } from '@pf_qnb_payment_gateway/js/qnb_options';
import paymentForm from '@payment/js/payment_form';

paymentForm.include({

    // #=== DOM MANIPULATION ===#

    /**
     * Prepare the inline form of Stripe for direct payment.
     *
     * @override method from @payment/js/payment_form
     * @private
     * @param {number} providerId - The id of the selected payment option's provider.
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The online payment flow of the selected payment option.
     * @return {void}
     */
    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'qnb') {
            this._super(...arguments);
            return;
        }

        // Check if instantiation of the element is needed.
        this.qnbElements ??= {}; // Store the element of each instantiated payment method.
        // Check if instantiation of the element is needed.
        if (flow === 'token') {
            return; // No elements for tokens.
        } else if (this.qnbElements[paymentOptionId]) {
            this._setPaymentFlow('direct'); // Overwrite the flow even if no re-instantiation.
            return; // Don't re-instantiate if already done for this provider.
        }

        // Overwrite the flow of the select payment option.
        this._setPaymentFlow('direct');

        // Extract and deserialize the inline form values.
        const radio = document.querySelector('input[name="o_payment_radio"]:checked');
        const inlineForm = this._getInlineForm(radio);

        const QnbForm = inlineForm.querySelector('[name="o_qnb_form"]');
        // this.stripeInlineFormValues = JSON.parse(
        //     QnbForm.dataset['QnbInlineFormValues']
        // );

        this.qnbElements[paymentOptionId] = JSON.parse(
            QnbForm.dataset['qnbInlineFormValues']
        );
        this.qnbElements[paymentOptionId].form = QnbForm;

    },

    // #=== PAYMENT FLOW ===#

    /**
     * Trigger the payment processing by submitting the elements.
     *
     * @override method from @payment/js/payment_form
     * @private
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The payment flow of the selected payment option.
     * @return {void}
     */
    async _initiatePaymentFlow(providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'qnb' || flow === 'token') {
            await this._super(...arguments); // Tokens are handled by the generic flow.
            return;
        }

        const inputs = Object.values(
            this._qnbGetInlineFormInputs(paymentOptionId, paymentMethodCode)
        );
        if (!inputs.every(element => element.reportValidity())) {
            this._enableButton(); // The submit button is disabled at this point, enable it
            return;
        }
        await this._super(...arguments);
    },

    // #=== GETTERS ===#

    /**
     * Return all relevant inline form inputs based on the payment method type of the provider.
     *
     * @private
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @return {Object} - An object mapping the name of inline form inputs to their DOM element
     */

    _qnbGetInlineFormInputs(paymentOptionId, paymentMethodCode) {
        const form = this.qnbElements[paymentOptionId]['form'];
        if (paymentMethodCode === 'card') {
            return {
                card: form.querySelector('#o_qnb_card'),
                month: form.querySelector('#o_qnb_month'),
                year: form.querySelector('#o_qnb_year'),
                code: form.querySelector('#o_qnb_code'),
            };
        } else {
            return {
                accountName: form.querySelector('#o_authorize_account_name'),
                accountNumber: form.querySelector('#o_authorize_account_number'),
                abaNumber: form.querySelector('#o_authorize_aba_number'),
                accountType: form.querySelector('#o_authorize_account_type'),
            };
        }
    },

    /**
     * Process Stripe implementation of the direct payment flow.
     *
     * @override method from payment.payment_form
     * @private
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {object} processingValues - The processing values of the transaction.
     * @return {void}
     */
    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'qnb') {
            await this._super(...arguments);
            return;
        }

        // Build the authentication and card data objects to be dispatched to Authorized.Net
        const secureData = {
            authData: {
                qnb_public_key: this.qnbElements[paymentOptionId]['public_key'],
                qnb_private_key: this.qnbElements[paymentOptionId]['private_key'],
            },
            ...this._qnbGetPaymentDetails(paymentOptionId, paymentMethodCode),
        };


        this.rpc('/payment/qnb/return', {
            'processing_data': processingValues,
            'payment_data': secureData
        })
        .then(function(result) {
            console.log("Success:", result);
            window.location = '/payment/status';
        })
        .catch(function(error) {
            console.error("Error:", error);
        });
        
    },

     /**
     * Return the credit card or bank data to pass to the Accept.dispatch request.
     *
     * @private
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @return {Object} - Data to pass to the Accept.dispatch request
     */
     _qnbGetPaymentDetails(paymentOptionId, paymentMethodCode) {
        const inputs = this._qnbGetInlineFormInputs(paymentOptionId, paymentMethodCode);
        if (paymentMethodCode === 'card') {
            return {
                cardData: {
                    cardNumber: inputs.card.value.replace(/ /g, ''), // Remove all spaces
                    month: inputs.month.value,
                    year: inputs.year.value,
                    cardCode: inputs.code.value,
                },
            };
        } else {
            return {
                bankData: {
                    nameOnAccount: inputs.accountName.value.substring(0, 22), // Max allowed by acceptjs
                    accountNumber: inputs.accountNumber.value,
                    routingNumber: inputs.abaNumber.value,
                    accountType: inputs.accountType.value,
                },
            };
        }
    },

    
    

});
