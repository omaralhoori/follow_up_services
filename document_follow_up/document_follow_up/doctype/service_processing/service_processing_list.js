// Copyright (c) 2023, Direct Direction for Information Technology and contributors
// For license information, please see license.txt

frappe.listview_settings["Service Processing"] = {
	before_render() {
		//frappe.set_route('Form', 'Service Processing', 'new-services-1')
		frappe.new_doc("Service Processing");
		// ['Form', 'Services', 'new-services-1']
       // frappe.set_route() // redirect to home
    },	
	//onload: function (list_view) {
	//	frappe.set_route('Form', 'Service Processing', 'new-services-1')
	//},
	//onload: function (list_view) {
	//	frappe.require("logtypes.bundle.js", () => {
	//		frappe.utils.logtypes.show_log_retention_message(list_view.doctype);
	//	});
	//},
};
