// Copyright (c) 2023, Direct Direction for Information Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Actions Finalize', {
	setup: function(frm) {
		frm.set_query("service_name", function() {
			return {
				filters: {
					'docstatus': '1',
					'service_status': 'Finalize'
				}
			};
		});
	},
});