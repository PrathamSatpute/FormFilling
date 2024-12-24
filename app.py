from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta
import random

class FormFiller:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        
    def generate_random_name(self):
        """Generate a realistic-looking full name"""
        first_names = ["John", "James", "Robert", "Michael", "William", "David", "Sarah", "Emma", "Emily", "Olivia"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def generate_phone_number(self):
        """Generate a valid 10-digit phone number"""
        return f"{random.randint(6,9)}" + ''.join([str(random.randint(0,9)) for _ in range(9)])
    
    def generate_email(self, name):
        """Generate a realistic email based on name"""
        name = name.lower().replace(" ", ".")
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        return f"{name}@{random.choice(domains)}"
    
    def generate_address(self):
        """Generate a realistic-looking address"""
        streets = ["Park Street", "Main Road", "MG Road", "Church Street", "Brigade Road"]
        cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]
        return f"{random.randint(1,999)}, {random.choice(streets)}, {random.choice(cities)}"
    
    def generate_pincode(self):
        """Generate a valid 6-digit pincode"""
        return str(random.randint(100000, 999999))
    
    def generate_dob(self):
        """Generate a realistic date of birth for someone between 18-60 years old"""
        today = datetime.now()
        days_in_year = 365.25
        max_age_days = int(60 * days_in_year)
        min_age_days = int(18 * days_in_year)
        random_days = random.randint(min_age_days, max_age_days)
        dob = today - timedelta(days=random_days)
        return dob.strftime("%d/%m/%Y")

    def fill_form(self, form_url, captcha_code="GNFPYC"):
        """Fill the form with the specific fields"""
        try:
            self.driver.get(form_url)
            time.sleep(2)  # Wait for form to load
            
            # Generate data
            full_name = self.generate_random_name()
            phone = self.generate_phone_number()
            email = self.generate_email(full_name)
            address = self.generate_address()
            pincode = self.generate_pincode()
            dob = self.generate_dob()
            
            # Take a screenshot of the empty form
            self.driver.save_screenshot("empty_form.png")
            
            # Find and fill each field
            form_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[type='tel'], textarea")
            
            for field in form_fields:
                # Get the question text from the parent element
                question_text = field.find_element(By.XPATH, "./ancestor::div[contains(@role, 'listitem')]//div[contains(@role, 'heading')]").text.lower()
                
                try:
                    if "name" in question_text:
                        field.send_keys(full_name)
                    elif "contact" in question_text or "phone" in question_text:
                        field.send_keys(phone)
                    elif "email" in question_text:
                        field.send_keys(email)
                    elif "address" in question_text:
                        print(f"Filling address field with: {address}")  # Debugging line
                        field.send_keys(address)
                        print(f"Address filled: {field.get_attribute('value')}")  # Confirm address is filled
                    elif "pin" in question_text:
                        field.send_keys(pincode)
                    elif "date of birth" in question_text or "dob" in question_text:
                        print(f"Filling DOB field with: {dob}")  # Debugging line
                        # Split the DOB into day, month, year
                        dd, mm, yyyy = dob.split('/')
                        # Find the specific input fields for DOB
                        dob_fields = field.find_elements(By.XPATH, "./ancestor::div[contains(@role, 'listitem')]//input")
                        if len(dob_fields) >= 3:
                            dob_fields[0].send_keys(dd)
                            dob_fields[1].send_keys(mm)
                            dob_fields[2].send_keys(yyyy)
                            print(f"DOB filled: {dd}/{mm}/{yyyy}")  # Confirm DOB is filled
                    elif "code" in question_text and "verify" in question_text:
                        field.send_keys(captcha_code)
                        
                except Exception as e:
                    print(f"Error filling field {question_text}: {str(e)}")
                    continue
            
            # Take a screenshot of the filled form
            self.driver.save_screenshot("filled_form.png")
            
            # Handle gender selection (radio buttons)
            gender_options = self.driver.find_elements(By.XPATH, "//div[contains(., 'Gender')]//following::div[@role='radio']")
            if gender_options:
                random.choice(gender_options).click()
            
            # Find and click submit button
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button']//span[contains(text(), 'Submit')]")))
            submit_button.click()
            
            # Wait for submission confirmation
            time.sleep(2)
            
            # Take a screenshot of the submitted form or confirmation page
            self.driver.save_screenshot("submitted_form.png")
            
            print("Form submitted successfully!")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            self.driver.quit()

# Example usage
if __name__ == "__main__":
    form_filler = FormFiller()
    form_url = "https://forms.gle/WT68aV5UnPajeoSc8"  # Replace with your form URL
    form_filler.fill_form(form_url)  # Optionally pass a different CAPTCHA code if needed