# Copyright (c) 2023, Direct Direction for Information Technology and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ServiceDelivery(Document):
	def before_save(self):
		if self.notified and self.delivered:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Delivered')
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_date", self.notified_date)
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_to", self.notified_to)
			frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date", self.delivered_date)
			frappe.db.set_value("Services", {"name":self.service_name}, "delivered_to", self.delivered_to)
		elif  self.notified and not self.delivered:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Notified')
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_date", self.notified_date)
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_to", self.notified_to)
			frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "delivered_to", '')
		elif self.delivered and not self.notified:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Delivered')
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_date", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_to", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date", self.delivered_date)
			frappe.db.set_value("Services", {"name":self.service_name}, "delivered_to", self.delivered_to)
		else:
			frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Done')
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_date", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "notified_to", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date", '')
			frappe.db.set_value("Services", {"name":self.service_name}, "delivered_to", '')

	def on_trash(self):
		frappe.db.set_value("Services", {"name":self.service_name}, "service_status", 'Done')
		frappe.db.set_value("Services", {"name":self.service_name}, "notified_date", '')
		frappe.db.set_value("Services", {"name":self.service_name}, "notified_to", '')
		frappe.db.set_value("Services", {"name":self.service_name}, "delivery_date", '')
		frappe.db.set_value("Services", {"name":self.service_name}, "delivered_to", '')
