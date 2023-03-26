# Copyright (c) 2023, Youssef Restom and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from frappe.contacts.doctype.contact.contact import get_contacts_linking_to,get_contact_details

class POSSMSTemplate(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_pos_sms(sales_invoice):
	invoice = sales_invoice
	mobile =""
	sms_template = frappe.get_single('POS SMS Template').sms_template
	inv_data = frappe.get_value('Sales Invoice',sales_invoice,['customer','customer_name','creation','grand_total'], as_dict=1)
	if not sms_template:
		sms_template = 'Dear customer. {} confirmed. We have received your payment of {} on {}.\nPrint a detailed invoice here: {}.'
	customer = inv_data.get('customer')
	contact_id = get_contacts_linking_to('Customer', customer)
	if contact_id:
		mobile = get_contact_details(contact_id[0].get("name")).get("contact_mobile") or ""
	invoice_amount = frappe.format(inv_data.get("grand_total"),{"fieldtype":"Currency"})
	date_time = inv_data.get("creation")
	formatted_date_time = date_time.strftime("%d %b %Y at %I:%M %p")
	url = "{}/sales_invoice_receipt/{}".format(frappe.utils.get_url(),invoice)
	anchor = "<a href={}>Invoice</a>".format(url)
	return dict(mobile_number=mobile,sms_message=sms_template.format(
		invoice,invoice_amount,formatted_date_time,url
	))