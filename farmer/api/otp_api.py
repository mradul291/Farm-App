
import frappe

import requests
import json
from frappe import _


@frappe.whitelist(allow_guest=True)
def send_otp(phone_number):
    termii_url = "https://api.ng.termii.com/api/sms/otp/generate"
    api_key = "TLvfIVBNgZsPiXYvUbmXbKlutRFbxDcyyZKHzpBHkmAMnJwfOmXBnvtJUHfiYJ"  # Make sure it's in site_config.json or env

    payload = {
        "api_key": api_key,
        "pin_type": "NUMERIC",
        "phone_number": phone_number,
        "pin_attempts": 3,
        "pin_time_to_live": 1,
        "pin_length": 4
    }

    try:
        response = requests.post(termii_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        frappe.log_error(f"OTP API Error: {str(e)}", "Termii OTP Error")
        frappe.throw("Failed to send OTP. Please try again.")




@frappe.whitelist(allow_guest=True)
def verify_otp(pin_id, otp):

    api_key = "TLvfIVBNgZsPiXYvUbmXbKlutRFbxDcyyZKHzpBHkmAMnJwfOmXBnvtJUHfiYJ"
    url = "https://api.ng.termii.com/api/sms/otp/verify"

    payload = {
        "api_key": api_key,
        "pin_id": pin_id,
        "pin": otp 
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        return {"message": result}

    except requests.RequestException as e:
        frappe.log_error(f"OTP Verification Error: {str(e)}", "Termii OTP Verification")
        frappe.throw(_("OTP verification failed. Please try again."))
