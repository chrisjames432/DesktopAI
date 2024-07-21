import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up headless chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Path to the chromedriver executable
chrome_service = Service('C:\\webdriver\\chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# URL of the website
url = 'https://finance.yahoo.com/quote/SPY/'

# Open the URL
driver.get(url)

# Wait for the page to load completely
time.sleep(5)

# Scroll to the bottom of the page to ensure all content is rendered
scroll_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(1920, scroll_height)

# Take screenshot
screenshot_path = 'screenshot.png'
driver.save_screenshot(screenshot_path)

# Close the WebDriver
driver.quit()

print(f"Screenshot saved to {screenshot_path}")
