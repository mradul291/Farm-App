import frappe
from frappe import _
from datetime import datetime, timedelta
import math
import json
#Adding the Data into Farmer Master from Registration fields

def create_farmer_for_user(user_email, phone, gender, location, id_type, id_number, bank_name, account_number, crops_processed, 
                           qty_processed_daily, equipments_used, unit, site):
    try:
        print("FIRST STEP")
        # Check if Farmer Master already exists
        if frappe.db.exists("Farmer Master", {"farmer": user_email}):
            frappe.logger().info(f"Farmer already exists for user {user_email}")
            return

        # Create Farmer Master entry
        farmer = frappe.get_doc({
            "doctype": "Farmer Master",
            "farmer": user_email,  # Link field to User doctype (email is user name)
            "phone_number": phone,
            "gender": gender,
            "Address": location,
            "id_type": id_type,
            "id_number": id_number,
            "bank_name": bank_name,
            "account_number": account_number,
            "crops_processed": crops_processed,
            "qty_processed_daily": qty_processed_daily,
            "equipments_used": equipments_used,
            "unit": unit,
            "site": site

        })
        farmer.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info(f"Farmer Master created for user {user_email}")

        return farmer.name

    except Exception as e:
        print("EROROR", e)
        frappe.log_error(frappe.get_traceback(), "Farmer Master Creation Failed")

# API 1: Create User with Farmer Master 

@frappe.whitelist(allow_guest=True)
def create_user():
    
    data = json.loads(frappe.request.data)

    #user type based Create Users
    user_type = data.get("user_type")

    if user_type == "farmer":
        return(create_user_farmer(data))
    elif user_type == "buyer":
        return(create_buyer_user(data))
    elif user_type == "vendor":
        return(create_vendor_user(data))

# Functions creates Buyers user
def create_buyer_user(data):
    # Required Fields
    required_fields = ["first_name", "last_name", "email", "new_password","phone", "gender"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return {"message": "Missing required fields", "status": 400, "missing_fields": missing_fields}
    
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["new_password"]
    phone = data["phone"]
    gender = data["gender"]

     # Check if user already exists
    if frappe.db.exists("User", email):
        return {"message": f"User {email} already exists", "status": 400}
    
    try:
        # Create User
        user = frappe.get_doc({
            "doctype": "User",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "send_welcome_email": 0,
            "enabled": 1,
            "new_password": password,
            "roles": [{"role": "Customer"}]
        })
        user.insert(ignore_permissions=True)
        
        # # Assign "Farmer" role
        # user.append("roles", {"role": "Customer"})
        # user.save(ignore_permissions=True)
        
        frappe.db.commit()
        return {
            "message": "User Created Successfully",
            "status": 201,
            "data": {
                "user_id": user.name
            }
        }
    
    except Exception as e:
        frappe.db.rollback()
        return {"message": "Internal Server Error", "status": 500, "error": str(e)}

def create_vendor_user(data):
    required_fields = ["first_name", "last_name", "email", "new_password","phone", "gender","account_type"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return {"message": "Missing required fields", "status": 400, "missing_fields": missing_fields}
    
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["new_password"]
    phone = data["phone"]
    gender = data["gender"]
    account_type = data["account_type"]
    supplier_name = data.get("company_name") if account_type == "Company" else f"{first_name} {last_name}"

     # Check if user already exists
    if frappe.db.exists("User", email):
        return {"message": f"User {email} already exists", "status": 400}
    
    try:
        # Create User
        user = frappe.get_doc({
            "doctype": "User",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "send_welcome_email": 0,
            "enabled": 1,
            "new_password": password,
            "roles": [{"role": "Supplier"}]
        })
        user.insert(ignore_permissions=True)

        # Create Supplier 
        supplier = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": supplier_name,
            "supplier_type": "Company" if account_type == "Company" else "Individual"
        })
        supplier.insert(ignore_permissions=True)

        
        frappe.db.commit()
        return {
            "message": "User Created Successfully",
            "status": 201,
            "data": {
                "user_id": user.name,
                "supplier_id": supplier.name
            }
        }
    
    except Exception as e:
        frappe.db.rollback()
        return {"message": "Internal Server Error", "status": 500, "error": str(e)}
       
# Functions creates user along with Farm and Farmer Type
def create_user_farmer(data):
    # Required Fields
    required_fields = ["first_name", "last_name", "email", "new_password","phone", "gender","location","site", "farm_name"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return {"message": "Missing required fields", "status": 400, "missing_fields": missing_fields}
    
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["new_password"]
    phone = data["phone"]
    gender = data["gender"]
    location = data["location"]
    site = data["site"]
    farm_name = data["farm_name"]


    
    "", "","","", ""
    # Optional Fields
    optional_fields = [  "id_type", "id_number", "bank_name", "account_number", 
        "crops_processed", "qty_processed_daily", "equipments_used", "unit",  "longitude", 
        "latitude", "crops", "actual_crops", "address"
    ]
    
    user_data = {field: data.get(field, "" if field not in ["crops", "actual_crops"] else []) for field in optional_fields}
    
    # Check if user already exists
    if frappe.db.exists("User", email):
        return {"message": f"User {email} already exists", "status": 400}
    
    try:
        # Create User
        user = frappe.get_doc({
            "doctype": "User",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "location": location,
            "send_welcome_email": 1,
            "enabled": 1,
            "new_password": password,
            "roles": [{"role": "Farmer"}]
        })
        user.insert(ignore_permissions=True)
        
        # # Assign "Farmer" role
        # user.append("roles", {"role": "Farmer"})
        # user.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        # Create Farmer and Farm Records
        farmer_id = create_farmer_for_user(
            email, phone, gender, location, user_data["id_type"], 
            user_data["id_number"], user_data["bank_name"], user_data["account_number"], user_data["crops_processed"], 
            user_data["qty_processed_daily"], user_data["equipments_used"], user_data["unit"], site
        )
        
        farm_id = create_farm(
            farm_name, user_data["longitude"], user_data["latitude"], user_data["crops"], 
            user_data["actual_crops"], farmer_id, site, email,user_data["address"]
        )
        
        is_farm_updated = update_farm_in_farmer(farmer_id, farm_id)
        
        if not is_farm_updated:
            return {"message": "Failed to create user", "status": 500}
        
        return {
            "message": "User Created Successfully",
            "status": 201,
            "data": {
                "user_id": user.name,
                "farmer_id": farmer_id,
                "farm_id": farm_id
            }
        }
    
    except Exception as e:
        frappe.db.rollback()
        return {"message": "Internal Server Error", "status": 500, "error": str(e)}

def update_farm_in_farmer(farmer_id, farm_id):
    try:
        # Fetch the farmer document
        farmer_doc = frappe.get_doc("Farmer Master", farmer_id)
        
        # Check if the child table 'farms' exists
        if not hasattr(farmer_doc, 'farms'):
            return False

        # Check if the farm is already present
        farm_exists = any(farm.farm == farm_id for farm in farmer_doc.farms)

        if not farm_exists:
            farm_doc = frappe.get_doc("Farm Master", farm_id)
            # Append new farm entry to the child table
            farmer_doc.append("farms", {
                "farm": farm_id,
                "farm_name": farm_doc.farm_name,  # Example field
                "longitude": farm_doc.longitude,          # Example field
                "latitude": farm_doc.latitude, # Example field
                "crops": farm_doc.crop_name,  # Example field
                "address": farm_doc.address,
                "document": farm_doc.documents,  # Example field
            })
            farmer_doc.save()
            frappe.db.commit()
            return True
        else:
            return False

    except Exception as e:
        frappe.log_error(f"Error updating farm in farmer: {str(e)}", "update_farm_in_farmer")
        return False

# @frappe.whitelist(allow_guest=True)
def create_farm(farm_name,longitude,latitude,crops,actual_crops,farmer_id,site, email,address):
    
    try:
        # Get JSON data from Postman request
        data = frappe.request.get_json()

        if not data:
            return {"status": "Failed", "message": "No JSON data provided."}

        # Validation
        if not (farm_name and longitude and latitude):
            return {"status": "Failed", "message": "Missing required fields."}

        # Prepare Table MultiSelect entries (crop_name field)
        crop_table = ''
        if crops and isinstance(crops, list):
            crop_table = ",".join(set(crops))
                

        # Prepare Actual Crop child table entries
        actual_crop_table = []
        if actual_crops and isinstance(actual_crops, list):
            for ac in actual_crops:
                if ac.get("crop_name"):
                    actual_crop_table.append({
                        "crop_name": ac.get("crop_name"),
                        "start_month": ac.get("start_month"),
                        "end_month": ac.get("end_month"),
                        "quantity": ac.get("quantity"),
                        "unit": ac.get("unit")
                    })

        # Create Farm Master entry
        farm = frappe.get_doc({
            "doctype": "Farm Master",
            "farm_name": farm_name,
            "associated_farmer":farmer_id,
            "site":site,
            "longitude": longitude,
            "latitude": latitude,
            "address": address, 
            "crop_name": crop_table,        # MultiSelect Table field
            "actual_crops": actual_crop_table  # Child Table field
        })

        print("******************************************************************************")
        print(address)
        farm.insert(ignore_permissions=True)  # Allow Guest
        frappe.db.set_value("Farm Master", farm.name, "owner", email)
        print(email)


        frappe.db.commit()

        return farm.name                                                                            

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Farm Creation Error")
        return {
            "status": "Failed",
            "message": f"Error occurred: {str(e)}"
        }
     
# API 3: Get All Crop Master Entries

@frappe.whitelist(allow_guest=True)
def get_all_crops():
    try:
        crops = frappe.get_all("Crops Master", fields=["name"])
        return {
            "status": "Success",
            "crops": crops
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Crop Fetch Error")
        return {
            "status": "Failed",
            "message": f"Error occurred: {str(e)}"
        }
    

# API 4: Get All Sites List

@frappe.whitelist(allow_guest=True)
def fetch_site_list():
    try:
        # Fetch all Site records
        site_list = frappe.get_all("Site", fields=["name", "site_name"])

        return {
            "status": "success",
            "data": site_list
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Fetch Site List Failed")
        return {
            "status": "error",
            "message": "Failed to fetch site list"
        }

# API 5: Check for the Farmer Specific Items

def item_permission_query_conditions(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
    else:
        return f"`tabItem`.owner = '{user}'"

# API 6: Create Website item during the Item Creation

def create_or_update_website_item(doc, method):
    if doc.show_on_website:
        
        # Check if Website Item exists
        website_item = frappe.db.exists("Website Item", {"item_code": doc.item_code})
        
        if website_item:
            website_item_doc = frappe.get_doc("Website Item", website_item)
        else:
            website_item_doc = frappe.new_doc("Website Item")
            website_item_doc.item_code = doc.item_code
        
        # Dynamically fetch matching fields and update
        item_fields = [field.fieldname for field in frappe.get_meta("Item").fields]
        website_item_fields = [field.fieldname for field in frappe.get_meta("Website Item").fields]
        
        for field in website_item_fields:
            if field in item_fields:
                website_item_doc.set(field, doc.get(field))
        
        website_item_doc.save(ignore_permissions=True)

        # --------------------------
        # Copy Attachments (Image/File)
        # --------------------------
        # Fetch all attachments from Item
        attachments = frappe.get_all("File", filters={
            "attached_to_doctype": "Item",
            "attached_to_name": doc.name
        }, fields=["name", "file_url", "file_name"])
        
        # Remove existing attachments in Website Item (optional, to avoid duplicates)
        existing_files = frappe.get_all("File", filters={
            "attached_to_doctype": "Website Item",
            "attached_to_name": website_item_doc.name
        }, fields=["name"])
        for file in existing_files:
            frappe.delete_doc("File", file.name, ignore_permissions=True)
        
        # Attach same files to Website Item
        first_file_url = ""
        for idx, file in enumerate(attachments):
            new_file = frappe.new_doc("File")
            new_file.file_url = file.file_url
            new_file.file_name = file.file_name
            new_file.attached_to_doctype = "Website Item"
            new_file.attached_to_name = website_item_doc.name
            new_file.save(ignore_permissions=True)
            
            # Store the first file's URL to set as website image
            if idx == 0:
                first_file_url = file.file_url

        
        # Set Website Item's website_image field
        if first_file_url:
            website_item_doc.website_image = first_file_url
            website_item_doc.save(ignore_permissions=True)

        website_item_url = f"/app/website-item/{website_item_doc.name}"

        frappe.msgprint(f"""<p>Website Item for <strong>{doc.item_code}</strong> has been created/updated with attachments.</p>
           <p>To add more details or update the product, <a href="{website_item_url}" target="_blank">Click here to update Website Item</a>.</p>""", title="Website Item Updated", indicator="green")
    
    else:
        # Remove Website Item if unchecked
        website_item = frappe.db.exists("Website Item", {"item_code": doc.item_code})
        if website_item:
            frappe.delete_doc("Website Item", website_item, ignore_permissions=True)
            frappe.msgprint(f"Website Item removed for {doc.item_code}")

# API 7: Sending the financing_available field data from Website item to Item and Sales order item.

@frappe.whitelist()
def get_financing_availability(sales_order):
    """Fetch financing availability for each item in Sales Order"""
    sales_order_doc = frappe.get_doc("Sales Order", sales_order)
    items_data = []

    for item in sales_order_doc.items:
        financing_available = frappe.get_value(
            "Website Item",
            {"item_code": item.item_code},
            "financing_available"
        )
        items_data.append({
            "item_code": item.item_code,
            "financing_available": financing_available or 0
        })

    return {"items": items_data}

# API 8: Check for User specific Loan Application

def loan_application_permission_query_conditions(user):
    if not user:
        user = frappe.session.user

    # Admin users can see all loan applications
    if "System Manager" in frappe.get_roles(user):
        return None  
      
    # Regular users can only see their own Loan Applications
    return f"`tabLoan Application`.owner = '{user}'"


# API 9: 

@frappe.whitelist(allow_guest=True)  # Requires user authentication
def upload_profile_picture():
    """Upload an image and set it as the user's profile picture using File doctype"""
    user_type = frappe.form_dict.get("user_type")

    user_email = frappe.form_dict.get("user_email")  # Get the logged-in user
    farmer_name = frappe.form_dict.get("farmer_id")  # Add as attachment then add to field - documents - Doctype - Farm Master
    farm_name = frappe.form_dict.get("farm_name")  # Add in attachment () Doctype - Farmer Master


    uploaded_file = frappe.request.files.get("profile_image")
    uploaded_farmer_id = frappe.request.files.get("id_document")
    uploaded_farm_doc = frappe.request.files.get("farm_document")

    if not uploaded_file:
        profile_image_url =  {"error": "No image file uploaded."}
    else:
        try:
            # Read file data
            file_data = uploaded_file.read()
            filename = uploaded_file.filename
            file_path = f"/files/{filename}"

            # Save file in File doctype
            file_doc = frappe.get_doc({
                'doctype': 'File',
                'file_name': filename,
                'attached_to_doctype': 'User',  # Attach to User doctype
                'attached_to_name': user_email,  # Attach to the logged-in user's document
                'file_url': file_path,  # File storage path
                'is_private': 0,  # Set to 1 if you want private file access
                'content': file_data  # Convert to base64
            })
            file_doc.insert(ignore_permissions=True)

            # Update the User profile with the uploaded image URL
            user_doc = frappe.get_doc("User", user_email)
            user_doc.user_image = file_doc.file_url
            user_doc.save(ignore_permissions=True)

            frappe.db.commit()

            profile_image_url =  file_doc.file_url

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Profile Picture Upload Failed")
            return {"error": f"Failed to upload image: {str(e)}","status":500}
    
    if not uploaded_farmer_id:
        farmer_id_url =  {"error": "No Id Document uploaded."}
    else:
        try:
            # Read file data
            file_data = uploaded_farmer_id.read()
            filename = uploaded_farmer_id.filename
            file_path = f"/files/{filename}"
            attached_doc = 'Farmer Master'
            if user_type == "vendor":
                attached_doc = "Supplier"
            # Save file in File doctype
            file_doc = frappe.get_doc({
                'doctype': 'File',
                'file_name': filename,
                'attached_to_doctype': attached_doc,  # Attach to User doctype
                'attached_to_name': farmer_name ,  # Attach to the logged-in user's document
                'file_url': file_path,  # File storage path
                'is_private': 0,  # Set to 1 if you want private file access
                'content': file_data  # Convert to base64
            })
            file_doc.insert(ignore_permissions=True)

            farmer_id_url = file_doc.file_url
            frappe.db.commit()

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Profile Picture Upload Failed")
            return {"error": f"Failed to upload image: {str(e)}","status":500}
    
    if not uploaded_farm_doc:
        farm_document_url =  {"error": "No image file uploaded."}
    else:
        try:
            # Read file data
            file_data = uploaded_farm_doc.read()
            filename = uploaded_farm_doc.filename
            file_path = f"/files/{filename}"

            # Save file in File doctype
            file_doc = frappe.get_doc({
                'doctype': 'File',
                'file_name': filename,
                'attached_to_doctype': 'Farm Master',  # Attach to User doctype
                'attached_to_name': farm_name,  # Attach to the logged-in user's document
                'file_url': file_path,  # File storage path
                'is_private': 0,  # Set to 1 if you want private file access
                'content': file_data  # Convert to base64
            })
            file_doc.insert(ignore_permissions=True)

            # Update the User profile with the uploaded image URL
            user_doc = frappe.get_doc("Farm Master", farm_name)
            user_doc.documents = file_doc.file_url
            user_doc.save(ignore_permissions=True)

            frappe.db.commit()
            farm_document_url = file_doc.file_url
            
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Profile Picture Upload Failed")
            return {"error": f"Failed to upload image: {str(e)}", "status":500}

    return {
            "message": "Profile picture updated successfully",
            "data":
                {"image_url": profile_image_url,
                "farmer_id_url":farmer_id_url,
                "farm_document": farm_document_url},
            "status":200
                }
# API 9: Check for User Specific Website Item View

def user_specific_website_item(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
    else:
        return f"`tabWebsite Item`.owner = '{user}'"
    
# API 9: Check for User Specific Farms 

def user_specific_farms(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
    else:
        return f"`tabFarm Master`.owner = '{user}'"
    
# 10: Check for User Specific Loan Installments 

def user_specific_loan_installments(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
    else:
        return f"`tabLoan Installments`.owner = '{user}'"
    
# # 11: Check for User Specific Crops  

# def user_specific_crops(user):
#     if not user: user = frappe.session.user
#     if "System Manager" in frappe.get_roles(user):
#         return None
#     else:
#         return f"`tabCrops Master`.owner = '{user}'"
    

# 12: Check for User Specific Sales Orders  

def user_specific_sales_order(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
    else:
        return f"`tabSales Order`.owner = '{user}'"
    
# 13: Check for User Specific Farmer Master  

def user_specific_farmer(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
    else:
        return f"`tabFarmer Master`.owner = '{user}'"