import json, time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

def scrape_bhubharati_live(district, mandal, village, survey_list):
    options = Options()
    # Critical Stability Flags for 2026 Mac Systems
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("detach", True) # KEY: Keeps the browser open even if the script ends
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="MacIntel",
        webgl_vendor="Apple Inc.",
        renderer="Apple M3 GPU",
        fix_hairline=True,
    )

    wait = WebDriverWait(driver, 25)

    try:
        print("🌍 Connecting to Bhu Bharati Gateway...")
        driver.get("https://bhubharati.telangana.gov.in/prohibitedProperties")
        
        # 1. Check for Login Redirect
        if "login" in driver.current_url:
            print("⚠️ REDIRECTED: Portal requires Login or Manual Navigation.")
            print("👉 Action: Click on 'Public Services' -> 'Prohibited Lands' in the browser.")
        
        # 2. Location Selection
        print("🔍 Searching for District Dropdown...")
        dist_el = wait.until(EC.presence_of_element_located((By.ID, "districtID")))
        Select(dist_el).select_by_visible_text(district)
        print(f"✅ Selected District: {district}")

        # (Rest of the loop logic stays the same)
        # ... 

    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # driver.quit() # COMMENTED OUT: Browser will now stay open for you to debug!

if __name__ == "__main__":
    # Updated to your local Rangareddy corridor
    scrape_bhubharati_live("Sangareddy", "Ramachandrapuram", "Kollur", ["130", "131", "135"])