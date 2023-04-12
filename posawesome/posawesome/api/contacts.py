import frappe

from frappe.contacts.doctype.contact.contact import get_default_contact,get_contact_details


@frappe.whitelist()
def sales_invoice_payload(customer):

    default_contact = get_default_contact("Customer", customer)

    email_accounts = [x.get("name") for x in frappe.get_all("Email Account",filters=dict(enable_outgoing=1),order_by='default_outgoing DESC')]
    
    return dict(email_accounts=email_accounts,contact_details=get_contact_details(default_contact) or {}, print_formats=[x.get("name") for x in frappe.get_all("Print Format", filters=dict(doc_type=["IN",["Sales Invoice","POS Invoice"]],standard='Yes'))] or [])
