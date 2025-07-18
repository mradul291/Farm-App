app_name = "farmer"
app_title = "Farmer"
app_publisher = "chirag"
app_description = "Farmer App"
app_email = "chirag@gmail.com"
app_license = "mit"


signup_form_template = "/public/frontend/index.html"


website_route_rules = [
    {"from_route": "/#signup", "to_route": "/public/frontend/index"}
]


app_include_js = "/assets/farmer/js/redirect.js"


# website_path_resolver = "farmer.utils.custom_resolver"

# on_logout = "farmer.utils.redirect_to_signup"


# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "farmer",
# 		"logo": "/assets/farmer/logo.png",
# 		"title": "Farmer",
# 		"route": "/farmer",
# 		"has_permission": "farmer.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/farmer/css/farmer.css"
# app_include_js = "/assets/farmer/js/farmer.js"

# include js, css files in header of web template
# web_include_css = "/assets/farmer/css/farmer.css"
# web_include_js = "/assets/farmer/js/farmer.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "farmer/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "farmer/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "farmer.utils.jinja_methods",
# 	"filters": "farmer.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "farmer.install.before_install"
# after_install = "farmer.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "farmer.uninstall.before_uninstall"
# after_uninstall = "farmer.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "farmer.utils.before_app_install"
# after_app_install = "farmer.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "farmer.utils.before_app_uninstall"
# after_app_uninstall = "farmer.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "farmer.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"farmer.tasks.all"
# 	],
# 	"daily": [
# 		"farmer.tasks.daily"
# 	],
# 	"hourly": [
# 		"farmer.tasks.hourly"
# 	],
# 	"weekly": [
# 		"farmer.tasks.weekly"
# 	],
# 	"monthly": [
# 		"farmer.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "farmer.install.before_tests"
# app_include_js = "/assets/farmer/js/registration.js"

# app_include_js = [
#     "assets/appname/js/customer_quick_entry.js"
# ]

# signup_form_template = "/www/registration/index.html"

define_csrf = 1

# doctype_js = {"Sales Order": "public/js/sales_order.js"}

permission_query_conditions = {
    "Item": "farmer.api.user_api.item_permission_query_conditions",
    "Loan Application": "farmer.api.user_api.loan_application_permission_query_conditions",
    "Website Item": "farmer.api.user_api.user_specific_website_item",
    "Farm Master": "farmer.api.user_api.user_specific_farms",
    "Loan Installments": "farmer.api.user_api.user_specific_loan_installments",
    # "Crops Master": "farmer.api.user_api.user_specific_crops",
    "Sales Order": "farmer.api.user_api.user_specific_sales_order",
    "Farmer Master": "farmer.api.user_api.user_specific_farmer",
    # "Sales Invoice": "farmer.api.user_api.user_specific_sales_invoice",
    "Business": "farmer.api.user_api.user_specific_business",
    "Warehouse": "farmer.api.user_api.user_specific_warehouse",
    "Sales Order": "farmer.api.user_api.get_permission_query_conditions",
    "Sales Invoice": "farmer.api.user_api.get_permission_query_conditions_sales_invoice",
    "Delivery Note": "farmer.api.user_api.user_specific_delivery_note",
    "Shipment": "farmer.api.user_api.user_specific_shipment",
    "User": "farmer.api.user_api.user_specific_user",
    "Case": "farmer.api.user_api.user_specific_cases",
    "Technician Task": "farmer.api.user_api.task_query_condition",
    "Technician": "farmer.api.user_api.technician_query_condition",
    "Site": "farmer.api.user_api.get_site_permission_query",
}

has_permission = {
    "Technician Task": "farmer.api.user_api.task_has_permission",
    "Technician": "farmer.api.user_api.technician_has_permission",
    "Site": "farmer.api.user_api.site_has_permission"
}

doc_events = {
    "Item": {
        "after_insert": "farmer.api.user_api.create_or_update_website_item",
        "on_update": "farmer.api.user_api.create_or_update_website_item"
    },
    "Loan Application": {
        "on_update": "farmer.api.loan_api.create_loan_installments"
    },
    "Payment Entry": {
        "on_submit": "farmer.api.sponsor_api.handle_payment_entry_submit",
    },
    "Business": {
        "on_update": "farmer.api.warehouse_api.create_warehouses_for_business"
    },
    "Warehouse": {
        "after_insert": "farmer.api.warehouse_api.link_warehouse_to_business"
    },
    "Sales Order": {
        "on_submit": "farmer.api.notification_api.notify_item_owners"
    },
    "Shipment": {
        "on_update": "farmer.api.delivery_api.notify_agent_on_assignment",
        "on_submit": "farmer.api.delivery_api.on_submit",
        "before_submit": "farmer.api.delivery_api.before_submit"
    },
    "Sales Invoice": {
        "on_submit": "farmer.api.sponsor_api.update_sponsor_quantities_on_invoice_submit",
        "on_cancel": "farmer.api.sponsor_api.reverse_sponsor_usage_on_invoice_cancel"
    },
    "User": {
        "after_insert": "farmer.api.technician_api.create_technician_from_user",
        "on_update":  "farmer.api.technician_api.sync_technician_from_user"
    },
    "Technician Task": {
        "on_update": "farmer.api.technician_api.send_assignment_email"
    },
    "Store Transfer": {
        "on_submit": "farmer.api.store_api.on_submit_store_transfer"
    }
}                                                                                                                                                                                                        


# Overriding Methods
# ------------------------------

override_whitelisted_methods = {
    # User Api's
     "farmer.api.user_api.create_user": "farmer.api.user_api.create_user",
     "farmer.api.user_api.login": "farmer.api.user_api.login",
     "farmer.api.user_api.create_farm": "farmer.api.user_api.create_farm",
     "farmer.api.user_api.get_all_crops": "farmer.api.user_api.get_all_crops",
     "farmer.api.user_api.fetch_site_list": "farmer.api.user_api.fetch_site_list",
     "farmer.api.user_api.get_financing_availability": "farmer.api.user_api.get_financing_availability",
     "farmer.api.user_api.create_sales_order": "farmer.api.user_api.create_sales_order",
     "farmer.api.user_api.get_all_equipment_items": "farmer.api.user_api.get_all_equipment_items",
     "farmer.api.user_api.get_total_user_crops_card": "farmer.api.user_api.get_total_user_crops_card",

    # Loan Api's
     "farmer.api.loan_api.make_loan_payment_request": "farmer.api.loan_api.make_loan_payment_request",
     "farmer.api.loan_api.make_installment_payment_request": "farmer.api.loan_api.make_installment_payment_request",
     "farmer.api.loan_api.create_invoice_from_sales_order": "farmer.api.loan_api.create_invoice_from_sales_order",
     "farmer.api.loan_api.refresh_loan_installments": "farmer.api.loan_api.refresh_loan_installments",

    # Test Api's
     "farmer.api.otp_api.send_otp": "farmer.api.otp_api.send_otp",
     "farmer.api.otp_api.verify_otp": "farmer.api.otp_api.verify_otp",
     
    # Sponsor Api's
     "farmer.api.sponsor_api.get_qualified_loan_applications": "farmer.api.sponsor_api.get_qualified_loan_applications"
}


override_doctype_class = {
    "Shipment": "farmer.api.shipment.CustomShipment"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "farmer.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["farmer.utils.before_request"]
# after_request = ["farmer.utils.after_request"]

# Job Events
# ----------
# before_job = ["farmer.utils.before_job"]
# after_job = ["farmer.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"farmer.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


website_route_rules = [{'from_route': '/Signup/<path:app_path>', 'to_route': 'Signup'},]