frappe.ready(() => {
    console.log("Loan Application Web Form Loaded");

    function getQueryParams() {
        let params = new URLSearchParams(window.location.search);
        return {
            sales_order: params.get("sales_order") || "",
            total_amount: params.get("total_amount") || "0",
            product_name: params.get("product_name") || "",
            item_code: params.get("item_code") || "",
        };
    }

    let queryParams = getQueryParams();
    console.log("Query Parameters Extracted:", queryParams);

    if (typeof frappe.web_form !== "undefined") {
        console.log("Web Form Object Exists");

        // Set values from query parameters
        frappe.web_form.set_value("sales_order", queryParams.sales_order);
        frappe.web_form.set_value("total_amount", queryParams.total_amount);
        frappe.web_form.set_value("product_name", queryParams.product_name);
        frappe.web_form.set_value("item_code", queryParams.item_code);

        // Fetch the "tier" from Item doctype using the item_code
        if (queryParams.item_code) {

            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Item",
                    name: queryParams.item_code
                },
                callback: function (response) {
                    if (response && response.message) {
                        let item = response.message;
                        console.log("Fetched Item Data:", item);
                        let tier = item.tier || "";
                        console.log("Fetched Tier:", tier);

                        // Set the tier_name field in Loan Application Web Form
                        frappe.web_form.set_value("tier_name", tier);

                        if (tier) {
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Tier Master",
                                    name: tier
                                },
                                callback: function (tierResponse) {
                                    if (tierResponse && tierResponse.message) {
                                        let tierMaster = tierResponse.message;
                                        let tierDetails = tierMaster.tier_details || [];

                                        console.log("Fetched Tier Details (Child Table):", tierDetails);

                                        window.cachedTierDetails = tierDetails;
                                        // Extract and clean tenure_months
                                        let tenureOptions = tierDetails
                                            .map(entry => entry.tenure_months)
                                            .filter(months => months)
                                            .map(String);

                                        // Remove duplicates
                                        tenureOptions = [...new Set(tenureOptions)];

                                        console.log("Setting Repayment Period Options via set_df_property:", tenureOptions);

                                        // Set the repayment_period options
                                        frappe.web_form.set_df_property("repayment_period", "options", tenureOptions);
                                        frappe.web_form.refresh_field("repayment_period");
                                        
                                    }
                                }
                            });
                        }
                    }
                }
            });
            // Fetch the logged-in user's email
            fetch("/api/method/frappe.auth.get_logged_user")
                .then(response => response.json())
                .then(userData => {
                    if (!userData || !userData.message) {
                        console.error("Failed to fetch logged-in user.");
                        return;
                    }

                    let userEmail = userData.message;
                    console.log("Logged-in User Email:", userEmail);


                    // Set the applicant field with the email
                    frappe.web_form.set_value("applicant", userEmail);

                    // Fetch user details (to get full name)
                    return fetch(`/api/resource/User/${userEmail}`);
                })
                .then(response => response.json())
                .then(userDetails => {
                    if (!userDetails || !userDetails.data) {
                        console.error("Failed to fetch user details.");
                        return;
                    }

                    let userName = userDetails.data.full_name || "";
                    console.log("Logged-in User Name:", userName);

                    // Set the applicant_name field with the user's full name
                    frappe.web_form.set_value("applicant_name", userName);
                })
                .catch(error => console.error("Error fetching user data:", error));
        } else {
            console.error("frappe.web_form is NOT available!");
        }
    }
});

// Use frappe.web_form.on to handle the change event for repayment_period
// Polling to check if the repayment_period field value changes and update interest_rate accordingly
let lastRepaymentPeriodValue = null;

setInterval(function () {
    let selectedTenure = frappe.web_form.get_value("repayment_period");

    // Check if the repayment period has changed
    if (selectedTenure !== lastRepaymentPeriodValue) {
        lastRepaymentPeriodValue = selectedTenure;
        console.log("Repayment Period Changed:", selectedTenure);

        // If there is a selected repayment period, find corresponding interest_rate
        if (selectedTenure) {
            let matchedRow = window.cachedTierDetails.find(entry => String(entry.tenure_months) === String(selectedTenure));

            if (matchedRow) {
                let interestRate = matchedRow.interest_rate || "";
                console.log("Matched Interest Rate:", interestRate);

                // Update the interest_rate field
                frappe.web_form.set_value("interest_rate", interestRate);
            } else {
                console.warn("No matching tenure found in Tier Details");
                frappe.web_form.set_value("interest_rate", "");
            }
        }
    }
}, 10); 