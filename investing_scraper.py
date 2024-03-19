from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    # Uncomment to run Chrome in headless mode
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def fetch_data(driver):
    # Navigate to the Investing.com economic calendar page
    driver.get('https://www.investing.com/economic-calendar/')

    # Wait for the data table to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "economicCalendarData"))
    )

    # Extract the rows from the table
    rows = driver.find_elements(By.XPATH, '//table[@id="economicCalendarData"]/tbody/tr[contains(@class, "js-event-item")]')

    # Initialize a list to hold all the data
    data = []

    # Loop through each row and extract the required data
    for row in rows:
        time = row.find_element(By.CLASS_NAME, 'time').text.strip()
        currency = row.find_element(By.CLASS_NAME, 'left.flagCur').text.strip()
        event = row.find_element(By.CLASS_NAME, 'event').text.strip()
        impact = len(row.find_elements(By.XPATH, './/td[contains(@class, "sentiment")]/i[contains(@class, "grayFullBullishIcon")]'))
        actual = row.find_element(By.CLASS_NAME, 'act').text.strip() if row.find_elements(By.CLASS_NAME, 'act') else 'N/A'
        forecast = row.find_element(By.CLASS_NAME, 'fore').text.strip() if row.find_elements(By.CLASS_NAME, 'fore') else 'N/A'
        previous = row.find_element(By.CLASS_NAME, 'prev').text.strip() if row.find_elements(By.CLASS_NAME, 'prev') else 'N/A'

        # Append the row data to the data list
        data.append([time, currency, event, impact, actual, forecast, previous])

    return data

def print_table(data):
    # Print the table headers
    print(f"{'Time':<10}{'Currency':<10}{'Event':<50}{'Impact':<10}{'Actual':<10}{'Forecast':<10}{'Previous':<10}")
    # Print each row of data
    for row in data:
        print(f"{row[0]:<10}{row[1]:<10}{row[2]:<50}{row[3]:<10}{row[4]:<10}{row[5]:<10}{row[6]:<10}")

if __name__ == "__main__":
    driver = setup_driver()
    data = fetch_data(driver)
    print_table(data)
    driver.quit()
