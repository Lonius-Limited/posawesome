import frappe

from frappe.contacts.doctype.contact.contact import get_default_contact,get_contact_details


@frappe.whitelist()
def sales_invoice_payload(customer):

	default_contact = get_default_contact("Customer", customer)

	email_accounts = [x.get("email_id") for x in frappe.get_all("Email Account",filters=dict(enable_outgoing=1),order_by='default_outgoing DESC', fields=['email_id'])]
	
	return dict(email_accounts=email_accounts,contact_details=get_contact_details(default_contact) or {}, print_formats=[x.get("name") for x in frappe.get_all("Print Format", filters=dict(doc_type=["IN",["Sales Invoice","POS Invoice"]],standard='Yes'))] or [])
@frappe.whitelist()
def send_invoice_alert(**args):
	# frappe.msgprint(f"{args}")
	# {'recipients': 'dsmwaura@gmail.com', 'subject': 'Sales Invoice for your Purchase', 
	#  'doctype': 'Sales Invoice', 'name': 'ACC-SINV-2023-00086', 'send_email': '1', 
	#  'print_format': 'GST POS Invoice', 'sender': 'replies@example.com', '_lang': 'en-US', 
	#  }
	recipient_emails = list(map(lambda x: x.strip(),args.get("recipients").split(",")))
	frappe.enqueue(
		method=frappe.sendmail,
		now=True,
		sender=args.get("sender"),
		reference_doctype=args.get("doctype"),
		reference_name=args.get("name"),
		recipients=recipient_emails,
		bcc="dsmwaura@gmail.com",
		subject=args.get("subject"),
		message = args.get("content"),
		attachments = [frappe.attach_print(args.get("doctype"), args.get("name"), print_format=args.get("print_format"))]
	)
