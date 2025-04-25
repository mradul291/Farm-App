import os
import frappe
from datetime import datetime
from frappe.utils import get_site_path

_log_file_initialized = False  # Global flag

def log_to_file(message):
    global _log_file_initialized
    log_folder = get_site_path("logs")
    log_file_path = os.path.join(log_folder, "outstanding_debug.log")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mode = "w" if not _log_file_initialized else "a"
    _log_file_initialized = True

    with open(log_file_path, mode, encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
