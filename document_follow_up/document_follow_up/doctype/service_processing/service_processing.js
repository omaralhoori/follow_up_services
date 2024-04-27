// Copyright (c) 2023, Direct Direction for Information Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Processing', {
	before_submit:function(frm) {
		//frm.set_value('already_processed' ,frm.doc.name );
	},
	setup: function(frm) {
		frm.dashboard.hide()
		//frm.set_query("service_name", function() {
		//});
		frm.set_query("service_name", function() {
			return {
				        
				query: "document_follow_up.document_follow_up.doctype.service_processing.service_processing.service_query",
				//filters: {
				//	company: frm.doc.company
				//}
			};
		});

	},
	onload: function (frm) {
		//frappe.set_route("Form", 'Service Processing', 'OUT-2023-00021');
		//frm.set_value("service_name", 'IN-2023-00015');
	},

	
	refresh: function (frm) {
		
		//if (frm.is_new()) return;
		frm.add_custom_button(__("Exit"), function () {
			frappe.set_route();
			window.location.reload();
		});
		frm.add_custom_button(__("New"), function () {
			//frappe.set_route('Form', 'Service Processing', 'new-service-processing-1')
			frappe.new_doc("Service Processing");
			//window.location.reload();
		});
	},

	//already_processed:function(frm) {
	service_name:function(frm) {
		console.log(frm.doc.name)
		let text = frm.doc.name;
		const myDocName = text.split("-");
		console.log(myDocName[0])

		//if (frm.is_new()){
		//	console.log('new')
		//}else{
		//	console.log('old')
		//}
		
		if (frm.doc.already_processed && myDocName[0] == 'new') {

			frappe.set_route("Form", 'Service Processing', frm.doc.already_processed);
			
		}


	},
});