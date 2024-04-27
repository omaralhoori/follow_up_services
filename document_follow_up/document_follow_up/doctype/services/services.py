# Copyright (c) 2023, Direct Direction for Information Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _, msgprint, scrub
from frappe.model.document import Document
from datetime import date


class Services(Document):
	def __init__(self, *args, **kwargs):
		super(Services, self).__init__(*args, **kwargs)

	def validate(self):
		pass

	def on_trash(self):
		pass
		srv_name = frappe.utils.cstr(self.service_name)
		#if srv_name[:3] != "PRV":
		#	status = frappe.db.get_value("Services", {"service_name":self.service_name}, "service_status")
		#	if status not in ('Draft'):
		#		frappe.throw(_("The service under processing , Cannot be deleted"))

	def on_submit(self):
		try:
			service_processing=frappe.get_doc(dict(
				doctype = 'Service Processing',
				service_name = self.name,
				service_date = self.date,
				created_by = self.user_created,
				related_entity = self.related_entity,
				sector = self.sector,
				client_name = self.client_name,
				related_client = self.related_client,
				topic = self.topic,
			)).insert(ignore_permissions=True)
		except frappe.DuplicateEntryError:
			# already exists, due to a reinstall?
			pass
		
		self.service_status='To Process'
		self.service_processing=service_processing.name
		self.update_service_status(process=service_processing.name)


	def on_cancel(self):
		status = frappe.db.get_value("Services", {"service_name":self.service_name}, "service_status")
		
		if status != 'To Process':
			frappe.throw(_("The service under processing , Cannot be canceled"))
		else:
			self.service_status='Draft'
			self.service_processing=''

			service_processing = frappe.db.delete("Service Processing", {"name":self.service_processing})
			self.update_service_status(cancel=1)


	def update_service_status (self,process = '', cancel=0):
		if cancel:
			frappe.db.set_value("Services", {"service_name":self.service_name}, "service_status", 'Draft')
			frappe.db.set_value("Services", {"service_name":self.service_name}, "service_processing", process)
		else:
			frappe.db.set_value("Services", {"service_name":self.service_name}, "service_status", 'To Process')
			frappe.db.set_value("Services", {"service_name":self.service_name}, "service_processing", process)

