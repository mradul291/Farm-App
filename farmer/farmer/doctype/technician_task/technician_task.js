frappe.ui.form.on('Technician Task', {
    refresh: function(frm) {
        const user = frappe.session.user;
        const isTechnician = frappe.user_roles.includes("Technician");
        const isCreator = frm.doc.owner === user;

        // === Technician Controls ===
        if (isTechnician && frm.doc.status === "Open") {
            frm.add_custom_button("Start Task", () => {
                frm.set_value("status", "In Progress");
                frm.save();
            });
        }

        if (isTechnician && frm.doc.status === "In Progress") {
            frm.add_custom_button("Mark Work Done", () => {
                frm.set_value("status", "Work Done");
                frm.save();
            });

            frm.add_custom_button("Escalate", () => {
                frm.set_value("status", "Escalated");
                frm.save();
            });
        }

        // === Creator/Admin Controls ===
        if (isCreator && frm.doc.status === "Work Done") {
            frm.add_custom_button("Confirm Completion", () => {
                frm.set_value("status", "Completed");
                if (!frm.doc.completion_date) {
                    frm.set_value("completion_date", frappe.datetime.get_today());
                }
                frm.save();
            });
        }

        // === Field Visibility Logic ===
        const showFeedbackFields = ["Work Done", "Completed"].includes(frm.doc.status);

        // Show/hide the 3 feedback-related fields
        ['completion_confirmed', 'feedback_rating', 'feedback_comment'].forEach(field => {
            frm.set_df_property(field, 'hidden', !showFeedbackFields);
        });

        // Make fields read-only for technician (not owner)
        if (isTechnician && !isCreator && showFeedbackFields) {
            ['completion_confirmed', 'feedback_rating', 'feedback_comment', 'completion_date'].forEach(field => {
                frm.set_df_property(field, 'read_only', 1);
            });
        }

        // Make fields editable for creator only in "Work Done" stage
        if (isCreator && frm.doc.status === "Work Done") {
            ['completion_confirmed', 'feedback_rating', 'feedback_comment'].forEach(field => {
                frm.set_df_property(field, 'read_only', 0);
            });
            frm.set_df_property('completion_date', 'read_only', 1);
        }

        // In "Completed" status → everyone sees read-only
        if (frm.doc.status === "Completed") {
            ['completion_confirmed', 'feedback_rating', 'feedback_comment', 'completion_date'].forEach(field => {
                frm.set_df_property(field, 'read_only', 1);
            });
        }
    },

    // Auto-set Completion Date when checkbox is ticked
    completion_confirmed: function(frm) {
        if (frm.doc.completion_confirmed && !frm.doc.completion_date) {
            frm.set_value('completion_date', frappe.datetime.get_today());
        } else if (!frm.doc.completion_confirmed) {
            frm.set_value('completion_date', null);
        }
    }
});
