// Copyright (c) 2023, Direct Direction for Information Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Services', {
	onload: function (frm) {

	},
	refresh: function (frm) {
		frm.dashboard.hide()
		//if (frm.is_new()) return;
		frm.add_custom_button(__("Exit"), function () {
			frappe.set_route();
			window.location.reload();
		//	frappe.set_route("List", frm.doc.reference_doctype, "Kanban", frm.doc.name);
		});
		frm.add_custom_button(__("New"), function () {
			frappe.new_doc("Services");
			//frappe.set_route('Form', 'Services', 'new-services-1')
		});
	},

});
