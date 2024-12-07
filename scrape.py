from selenium.webdriver import Remote, ChromeOptions
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException

# Authentication and Proxy Configuration
AUTH = 'brd-customer-hl_9592450e-zone-scraping_browser2:t0iq92qzbpo3'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print('Connecting to Scraping Browser...')
    options = ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode for efficiency
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        # Connect to the remote web driver
        with Remote(command_executor=SBR_WEBDRIVER, options=options) as driver:
            driver.set_page_load_timeout(120)  # Set a timeout for page load
            print('Connected! Navigating...')
            
            # Navigate to the target website
            driver.get(website)
            
            # Optional: Solve Captcha if present
            try:
                solve_res = driver.execute_cdp_cmd(
                    "Captcha.waitForSolve",
                    {
                        "cmd": "Captcha.waitForSolve",
                        "params": {"detectTimeout": 10000}
                    }
                )
                print("Captcha solved:", solve_res)
            except Exception as e:
                print("Captcha handling failed or not required:", e)
            
            # Get page source
            html = driver.page_source
            return html
    except TimeoutException:
        print("Page load timeout. Check the URL or increase timeout.")
        return ""
    except WebDriverException as e:
        print("WebDriver error:", e)
        return ""
    except Exception as e:
        print("An unexpected error occurred:", e)
        return ""

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):  # Fix typo ("scripts" to "script")
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    print(cleaned_content)

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i: i+max_length] for i in range(0, len(dom_content), max_length)]























# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# import os

# load_dotenv()

# SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")


# def scrape_website(website):
#     print("Connecting to Scraping Browser...")
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print("Waiting captcha to solve...")
#         solve_res = driver.execute(
#             "executeCdpCommand",
#             {
#                 "cmd": "Captcha.waitForSolve",
#                 "params": {"detectTimeout": 10000},
#             },
#         )
#         print("Captcha solve status:", solve_res["value"]["status"])
#         print("Navigated! Scraping page content...")
#         html = driver.page_source
#         return html


# def extract_body_content(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     body_content = soup.body
#     if body_content:
#         return str(body_content)
#     return ""


# def clean_body_content(body_content):
#     soup = BeautifulSoup(body_content, "html.parser")

#     for script_or_style in soup(["script", "style"]):
#         script_or_style.extract()

#     # Get text or further process the content
#     cleaned_content = soup.get_text(separator="\n")
#     cleaned_content = "\n".join(
#         line.strip() for line in cleaned_content.splitlines() if line.strip()
#     )

#     return cleaned_content


# def split_dom_content(dom_content, max_length=6000):
#     return [
#         dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
#     ]