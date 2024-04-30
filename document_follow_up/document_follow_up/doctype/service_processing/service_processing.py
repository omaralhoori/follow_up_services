# Copyright (c) 2023, Direct Direction for Information Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _, msgprint, scrub
from frappe.model.document import Document
from datetime import date

class ServiceProcessing(Document):
	def validate(self):
		pass 
	@frappe.whitelist()
	def show_service_procedure(self):
		return frappe.local.conf.show_service_procedure
	def before_save(self):
		self.already_processed = self.name
		frappe.db.set_value("Services", {"name":self.service_name}, "service_processing",self.name)
		if self.period != 'Other':
			self.actual_period=self.period
		
		if self.delivery_date:
			frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date", self.delivery_date)
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'On Process')

		if self.received_administration:
			frappe.db.set_value("Services", {"name":self.service_name}, "secretary_name", self.received_administration)

		if self.start_process_date:
			frappe.db.set_value("Services", {"name":self.service_name}, "start_process_date", self.start_process_date)

		if self.end_process_date:
			frappe.db.set_value("Services", {"name":self.service_name}, "end_process_date", self.end_process_date)

		if self.process_finish:
			frappe.db.set_value("Services", {"name":self.service_name}, "process_finish", self.process_finish)
			if self.process_finish == "Yes":
				frappe.db.set_value("Services", {"name":self.service_name}, "service_status", "Done")

		if self.sector:
			frappe.db.set_value("Services", {"name":self.service_name}, "sector", self.sector)

		if self.decision_date or self.decision:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Done')
			frappe.db.set_value("Services", {"name":self.service_name}, "decision", self.decision)
			frappe.db.set_value("Services", {"name":self.service_name}, "reject_reason", self.reject_reason)
			frappe.db.set_value("Services", {"name":self.service_name}, "decision_date", self.decision_date)

	def on_trash(self):
		frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Draft')
		frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date",None)
		frappe.db.set_value("Services", {"name":self.service_name}, "start_process_date",None)
		frappe.db.set_value("Services", {"name":self.service_name}, "end_process_date",None)
		frappe.db.set_value("Services", {"name":self.service_name}, "process_finish","No")
		frappe.db.set_value("Services", {"name":self.service_name}, "sector", None)
		frappe.db.set_value("Services", {"name":self.service_name}, "decision", None)
		frappe.db.set_value("Services", {"name":self.service_name}, "reject_reason", None)
		frappe.db.set_value("Services", {"name":self.service_name}, "decision_date", None)
	
	

@frappe.whitelist()
def service_query(doctype, txt, searchfield, start, page_len, filters):
	#filters = frappe._dict(filters)

	return frappe.db.sql("""select name, client_name ,client_phone , related_entity , related_client from `tabServices`
		where ({key} like %(txt)s
				or client_name like %(txt)s
				or client_phone like %(txt)s
				or related_entity like %(txt)s
				or related_client like %(txt)s)
		order by
			name desc
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': 50})
	