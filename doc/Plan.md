# Tanner and Cuong's Project Plan
# Financial Advisor


## Description
* A web/mobile application that uses recorded personal spending habits and incomes to create a manageable financial plan. 

## Learning Goals
* Front-end development with React/Node/Vue/etc.
* Server implementations in Java or some other PLs (Linux server most likely; FastAPI if Python server)
* Money handling skills and algorithms
* Back-end development with new PLs (Rust, etc.)

## Feature Goals
* Essential
    * pages to manually enter past income and expenses [Done]
    * Show a chart of percentage expenses by expense category [In progress]
    * Dashboard for navigation (using Vue) [Needs work]
* Nice-to-Have
    * Automatically calculate supposed wealth and compare it to a user statement of wealth to alert for unaccounted incomes/expenditures
    * Comparison to a statistic based/user desired normal expense chart, and highlight overspending/underspending per category.
    * Calculators to simulate future wealth if saved (savings, retirement accounts, etc.) [Starting]
    * Server to hold expense data [Done]
    * Login/Account feature using server [Starting]
    * Page for budget creation, can help with the alerts
* Stretch
    * OCR implementation
    * Web-scraping for stock information to recommend investment options with liquid assets
    * Chatbot companion to help navigate the app
    * Combo of Financial Advisor and Fantasy Football Assistant
* Feedbacks
    * search function for expenses and plans
    * number inputs should support decimals and strip symbols like '$'
    * Add dummy database for expenses and savings so Jeff will have an easier time testing things out
    *  Clicking something deletes the pir chart? [Couldn't replicate bug so far]
    * Bigger graphs, with backgrounds and/or recolor for redability. Display both at once would be nice
    * Adding duplicate categories has SQLAlchemy error in console, add that to app
    * Budget shows exceeded by how much
    * A way to show everything at once
    * Text explanation of savings selection for those unfamiliar with finance
    * About page/add to home page
    * Maybe login feature
    * Alert on expenses page when budget exceeded
    * Editing features for expenses and savings
    * Savings crashes when final value is too large
* Completed feedbacks
    * (Done) Left justify input contents, right justify money
    * (Done) Less garish colors
    * (Done) Category dropdown can be tabbed to
    * (Done) Cat add menu has black text
    * (Done) More spacing for savings plan

## Project Architecture
* Dashboard with feature buttons
* Page for each feature
* Expense data server
* Nice-to-Have
    * Login screen
    * Server to hold login/account information
    * Other feature buttons from Nice-to-Have

## Development Schedule
* Discussing data specificity/what data we want to measure
* Tool setup, Hello World basics, Database w trivial content, home page template, server talks w file system and database (by week 4)
    * FastAPI of Python for server; 
* Database Design (by week 4)
* Chart development (parallel1) (by week 4)
* OCR implementation (parallel1)
* Data server (parallel2) (by week 7)
* Dashboard (UI) (parallel2) (by week 7)
* Nice-to-Have (if time)
    * Dashboard additions from Nice-to-Have features
    * Login/Account server
    * Better UI (light/dark mode) (parallel to everything)

## Concerns
* SCALE
* Finding or coming up with data, algorithms, etc. 
* UI development
* Find APIs to pull accurate spending and investment data (for stretch goal)

## Communication Plan
* Preferred method of communication is Slack
* Meet weekly or biweekly to discuss plans for the week/pair programming
* Meet before/after class briefly

## Contribution Plan
* Sit next to each other in class to feel the resentment from the other person
* Discuss weekly contributions during meeting times
* Add more to this plan as the term progresses

