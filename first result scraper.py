import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_first_video_link_selenium(search_query):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    try:
        base_url = "https://www.youtube.com/results?search_query="
        search_url = base_url + '+'.join(search_query.split())
        
        driver.get(search_url)
        # Wait for a moment to load the page
        time.sleep(0.5)
        
        # Find video links - update the selector based on YouTube's current structure
        video_elements = driver.find_elements(By.XPATH, "//a[@id='video-title']")
        
        if video_elements:
            # Get the href attribute of the first video
            href = video_elements[0].get_attribute('href')
            return href
        return None
    finally:
        driver.quit()

def process_queries(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='replace') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            search_query = line.strip()
            if search_query:
                print(f"Processing: {search_query}")
                try:
                    video_link = get_first_video_link_selenium(search_query)
                    if video_link:
                        outfile.write(f"{search_query}: {video_link}\n")
                    else:
                        outfile.write(f"{search_query}: No video found\n")
                except Exception as e:
                    outfile.write(f"{search_query}: Error - {str(e)}\n")
                    print(f"Error processing {search_query}: {e}")

# Example usage
input_file = "New Text Document.txt"
output_file = "results.txt"
process_queries(input_file, output_file)
