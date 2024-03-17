import re
import requests

def check_email(email):
    # Regular expression pattern for validating email addresses
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Use the re.match function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

def check_pass(password):
    if len(password) >= 8 and len(password) <= 20:
        return True
    else:
        return False