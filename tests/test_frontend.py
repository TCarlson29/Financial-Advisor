# testing frontend
from playwright.sync_api import sync_playwright

def clear_all_expenses(request_context):
    # fetch the full list…
    resp = request_context.get("/api/expenses")
    for exp in resp.json():
        # …and delete one by one
        dr = request_context.delete(f"/api/expenses/{exp['id']}")

def test_expenses_entry():
    with sync_playwright() as p:
        # —–––– make a standalone API context pointed at your backend –––––
        api = p.request.new_context(base_url="http://localhost:8000")
        clear_all_expenses(api)

        # —–––– now drive the GUI –––––
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:5173/")
        page.locator("text=Open").click()
        page.wait_for_url("**/expense-tracker")

        # make sure the table really is empty with only 4 filter <td>
        assert page.locator("td").count() == 4

        # add one…
        page.locator('input[placeholder="Expense name"]').fill("Groceries")
        page.locator('button', has_text="Select").click()
        page.locator('span[class="name"]', has_text="Food").click()
        page.locator('input[placeholder="Cost"]').fill("100")
        page.locator("button", has_text="Add").click()

        # and assert exactly one row (plus 4 from default)
        row = page.locator("tbody tr")
        assert row.locator("td").nth(4).inner_text() == "Groceries"
        assert row.locator("td").nth(5).inner_text() == "Food"
        assert row.locator("td").nth(6).inner_text() == "100.00"
        assert row.count() == 2

        browser.close()
        api.dispose()

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

# def test_expenses_entry():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()

#         # Go to homepage
#         page.goto("http://localhost:5173/")

#         # Click button to go to /todo-app
#         page.locator("text=Open").click()
#         page.wait_for_url("**/expense-tracker")

#         # Wait for the form fields to be visible
#         page.locator('input[placeholder="Expense name"]').wait_for()
#         page.locator('input[placeholder="Cost"]').wait_for()

#         # Fill form inputs
#         page.locator('input[placeholder="Expense name"]').fill("Groceries")
#         page.locator('input[placeholder="Cost"]').fill("100")

#         # Submit the form
#         page.locator('button', has_text="Add").click()

#         # Assert results visible
#         page.locator("text=Groceries").first.wait_for()  # Ensure the name is visible
#         page.locator("text=100.00").wait_for()  # Ensure the cost is visible

#         # Assertions to check visibility
#         row = page.locator("tr").last   # the last row in the table
#         assert row.locator("td", has_text="Groceries").is_visible()
#         assert row.locator("td", has_text="100.00").is_visible()

#         browser.close()

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
