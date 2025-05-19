frappe.ui.form.on('Business', {
    business_type: function(frm) {
        if (frm.doc.business_type === 'Farmer') {
            frm.set_value('reference_doctype', 'Farmer Master');
        } else if (frm.doc.business_type === 'Vendor') {
            frm.set_value('reference_doctype', 'Supplier');
        } else {
            frm.set_value('reference_doctype', '');
        }
    }
});
