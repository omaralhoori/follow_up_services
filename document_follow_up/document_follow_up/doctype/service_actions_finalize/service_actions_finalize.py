# Copyright (c) 2023, Direct Direction for Information Technology and contributors
# For license information, please see license.txt


from __future__ import unicode_literals

import frappe
from frappe import _, msgprint, scrub
from frappe.model.document import Document
from datetime import date

class ServiceActionsFinalize(Document):
	def __init__(self, *args, **kwargs):
		super(ServiceActionsFinalize, self).__init__(*args, **kwargs)

	def validate(self):
		pass

	def before_save(self):
		finalized_date = frappe.db.get_value("Services", {"name":self.service_name}, "finalized_date")
		if not finalized_date:
			frappe.db.set_value("Services", {"name":self.service_name}, "finalized_date", self.finalize_date)

	def on_trash(self):
		frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'On Process')
		frappe.db.set_value("Services", {"name":self.service_name}, "decision", '')
		frappe.db.set_value("Services", {"name":self.service_name}, "finalized_date", None)
		frappe.db.set_value("Services", {"name":self.service_name}, "decision_date", None)
		if frappe.db.exists("Service Processing",{"service_actions_finalize":self.name}):
			frappe.db.set_value("Service Processing", {"service_actions_finalize":self.name}, "docstatus",0)
			frappe.db.set_value("Service Processing", {"service_actions_finalize":self.name}, "service_actions_finalize",'')
			



	def on_submit(self):
		self.update_service_status()


	def on_cancel(self):
		if frappe.db.exists("Service Delivery",{"service_name":self.service_name}):
			frappe.throw(_("The service under delivery , Cannot be canceled"))
		else:
			self.update_service_status(cancel=1)

	def update_service_status (self,process='', cancel=0):
		if cancel:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Finalize')
			frappe.db.set_value("Services", {"name":self.service_name}, "decision", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "decision_date", None)
			#frappe.db.set_value("Service Processing", {"name":self.name}, "service_actions_finalize", process)
			#frappe.db.set_value("Service Processing", {"name":self.name}, "service_actions_finalize", process)
		else:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Done')
			frappe.db.set_value("Services", {"name":self.service_name}, "decision", self.decision)
			frappe.db.set_value("Services", {"name":self.service_name}, "decision_date", date.today())
			#frappe.db.set_value("Service Processing", {"name":self.name}, "service_actions_finalize", process)

			if self.amended_from:
				if frappe.db.exists("Service Processing",{"service_actions_finalize":self.amended_from}):
					frappe.db.set_value("Service Processing", {"service_actions_finalize":self.amended_from}, "service_actions_finalize", self.name)
			else:
				if frappe.db.exists("Service Processing",{"service_actions_finalize":self.name}):
					frappe.db.set_value("Service Processing", {"service_actions_finalize":self.name}, "service_actions_finalize", self.name)

