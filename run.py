
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import os
import time

def download_mp4(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Opening browser...")
        driver.get(url)
        
        # Wait for initial page load
        time.sleep(5)
        
        # Try multiple selectors
        selectors = [
            

            "//a[@data-btn-icon='q'][contains(., 'Play')]",
           
        ]
        
        play_button = None
        for selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                elements = driver.find_elements(By.XPATH, selector)
                print(f"Found {len(elements)} elements")
                if elements:
                    for element in elements:
                        print(f"Found element: {element.get_attribute('outerHTML')}")
                    play_button = elements[0]
                    break
            except Exception as e:
                print(f"Error with selector {selector}: {str(e)}")
                continue
        
        if play_button:
            print("Found play button, attempting to click...")
            # Try multiple click methods
            try:
                play_button.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", play_button)
                except:
                    actions = webdriver.ActionChains(driver)
                    actions.move_to_element(play_button).click().perform()
            
            print("Waiting for media to load...")
            time.sleep(10)
        else:
            print("Could not find play button")
        
        print("Getting performance logs...")
        logs = driver.get_log("performance")
        
        mp4_urls = set()
        for entry in logs:
            try:
                url_match = re.search(r'https?://[^\s<>"]+?\.mp4', str(entry))
                if url_match:
                    mp4_urls.add(url_match.group())
            except:
                continue
        
        print(f"Found {len(mp4_urls)} MP4 URLs")
        for mp4_url in mp4_urls:
            print(f"Found MP4: {mp4_url}")
            try:
                response = requests.get(mp4_url, stream=True)
                if response.status_code == 200:
                    filename = os.path.join(output_dir, mp4_url.split('/')[-1])
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Successfully downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading {mp4_url}: {str(e)}")
        
        input("Press Enter to close the browser...")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to close the browser...")
    finally:
        driver.quit()



# Example usage
url = "https://www.jiosaavn.com/song/raanjhan/Fz8qYCBZDh4"
download_mp4(url)