frappe.ui.form.on('Technician Task', {
    refresh(frm) {
        const user = frappe.session.user;
        const isCreator = frm.doc.owner === user;
        const isTechnician = frappe.user_roles.includes("Technician");

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

        if (isCreator && frm.doc.status === "Work Done") {
            frm.add_custom_button("Confirm Completion", () => {
                if (!frm.doc.completion_confirmed) {
                    frappe.msgprint({
                        title: __("Action Required"),
                        message: __("Tick <b>Completion Confirmed</b> before completing the task."),
                        indicator: "orange"
                    });
                    return;
                }
                frm.set_value("status", "Completed");
                if (!frm.doc.completion_date) {
                    frm.set_value("completion_date", frappe.datetime.get_today());
                }
                frm.save();
            });
        }

        const feedbackFields = ['completion_confirmed', 'feedback_rating', 'feedback_comment'];
        const showFeedback = ['Work Done', 'Completed'].includes(frm.doc.status);

        feedbackFields.forEach(f => frm.set_df_property(f, 'hidden', !showFeedback));

        if (isTechnician && !isCreator && showFeedback) {
            [...feedbackFields, 'completion_date'].forEach(f => frm.set_df_property(f, 'read_only', 1));
        }

        if (isCreator && frm.doc.status === "Work Done") {
            feedbackFields.forEach(f => frm.set_df_property(f, 'read_only', 0));
            frm.set_df_property('completion_date', 'read_only', 1);
        }

        if (frm.doc.status === "Completed") {
            const allFields = [...feedbackFields, 'completion_date'];
            allFields.forEach(f => {
                const readOnly = isCreator ? (f === 'completion_date') : 1;
                frm.set_df_property(f, 'read_only', readOnly);
            });
        }
    },

    validate(frm) {
        if (frm.doc.status === "Completed" && !frm.doc.completion_confirmed) {
            frappe.throw(__("Completion cannot be set to <b>Completed</b> unless <b>Completion Confirmed</b> is ticked."));
        }
    },

    completion_confirmed(frm) {
        if (frm.doc.completion_confirmed && !frm.doc.completion_date) {
            frm.set_value('completion_date', frappe.datetime.get_today());
        } else if (!frm.doc.completion_confirmed) {
            frm.set_value('completion_date', null);
        }
    }
});
