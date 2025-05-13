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
        assert "/expense-tracker" in page.url

        browser.close()

def test_expenses_entry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to homepage
        page.goto("http://localhost:5173/")

        # Click button to go to /todo-app
        page.locator("text=Open").click()
        page.wait_for_url("**/expense-tracker")

        # Wait for the form fields to be visible
        page.locator('input[placeholder="Expense name"]').wait_for()
        page.locator('input[placeholder="Cost"]').wait_for()

        # Fill form inputs
        page.locator('input[placeholder="Expense name"]').fill("Groceries")
        page.locator('input[placeholder="Cost"]').fill("100")

        # Submit the form
        page.locator('button', has_text="Add").click()

        # Assert results visible
        page.locator("text=Groceries").wait_for()  # Ensure the name is visible
        page.locator("text=100.00").wait_for()  # Ensure the cost is visible

        # Assertions to check visibility
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
