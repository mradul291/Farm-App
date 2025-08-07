frappe.ui.form.on('Insurance Claim', {
    after_save: function(frm) {
        if (!frm.doc.claim_id && frm.doc.name) {
            frm.set_value('claim_id', frm.doc.name);
            frm.save(); 
        }
    }
});
