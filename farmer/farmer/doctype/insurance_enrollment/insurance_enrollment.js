frappe.ui.form.on('Insurance Enrollment', {
    after_save: function(frm) {
        if (!frm.doc.enrollment_id && frm.doc.name) {
            frm.set_value('enrollment_id', frm.doc.name);
            frm.save(); 
        }
    }
});
