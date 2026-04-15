import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    raw_urls = os.environ.get("STREAMLIT_URLS", "")
    urls = [url.strip() for url in raw_urls.split(",") if url.strip()]

    if not urls:
        print("No URLs found. Please check your GitHub Secrets.")
        return

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for url in urls:
        print(f"\nTargeting: {url}")
        try:
            driver.get(url)
            
            wait = WebDriverWait(driver, 15)
            try:
                button_xpath = "//button[contains(text(),'Yes, get this app back up')]"
                button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button.click()
                print(f"Status: Wake-up button clicked for {url}")
                time.sleep(2) # Allow process to trigger
            except:
                print(f"Status: App is already awake or button not found.")

        except Exception as e:
            print(f"Error processing {url}: {e}")

    driver.quit()
    print("\nAll apps processed.")

if __name__ == "__main__":
    main()
