# testing frontend
from playwright.sync_api import sync_playwright
# from applitools.playwright import Eyes, Target

# pip install playwright
# pip3 install eyes-playwright
# pip install pytest
# playwright install

def test_navigation_todo_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open vue app
        page.goto("http://localhost:5173/")

        # click the "Open" button to go to the expenses page
        page.get_by_text("Open").click()
        
        # checks the url for the correct navigation
        assert "/todo-app" in page.url

        browser.close()

def test_expenses_entry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to web page
        page.goto("http://localhost:5173/")
        page.get_by_text("Open").click()

        # Fill form fields
        page.locator('#ActivityName').fill("Groceries")
        page.locator('#Amount').fill("100")

        # Click the Add button
        page.locator('#Add').click()

        # Wait for the new item to appear (adjust selector as needed)
        assert page.locator("text=Groceries").is_visible()
        assert page.locator("text=100.00").is_visible()

        browser.close()

# def test_fake_login():
#     with sync_playwright as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()

#         # Open vue app
#         page.goto("http://localhost:5173/")
#         # looks for login credentials
#         page.locator('id=username').fill("t-money")
#         page.locator('id=password').fill("testlogin123")
#         page.locator('id=log in').click()

#         assert "/todo-app" in page.url or page.locator("Add").is_visible()

#         browser.close()
