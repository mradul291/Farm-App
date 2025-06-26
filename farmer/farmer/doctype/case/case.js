frappe.ui.form.on("Case", {
  onload: function (frm) {
    // Set filter for user_type field
    frm.set_query("user_type", () => {
      return {
        filters: {
          name: ["in", ["Farmer Master", "Supplier"]],
        },
      };
    });

    // Set assigned_by to the currently logged-in user
    if (frm.is_new() && !frm.doc.assigned_by) {
      frm.set_value("assigned_by", frappe.session.user);
    }
  },
  //Fetching the Assigned User Email
  assigned_to: function (frm) {
    if (frm.doc.user_type && frm.doc.assigned_to) {
      // Define the primary field to fetch based on user_type
      let primary_field = frm.doc.user_type === "Farmer Master" ? "farmer" : "supplier";

      // First fetch the preferred field (farmer/supplier)
      frappe.call({
        method: "frappe.client.get_value",
        args: {
          doctype: frm.doc.user_type,
          filters: { name: frm.doc.assigned_to },
          fieldname: [primary_field, "owner"]  // fetch both
        },
        callback: function (r) {
          if (r.message) {
            // Use primary field if it has value, else fallback to owner
            let user_email = r.message[primary_field] || r.message.owner;
            frm.set_value("assigned_user_email", user_email);
          }
        }
      });
    }
  },
});
