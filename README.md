# Financial-Advisor

## Description

Our project is a small-scale financial app that can help you save, budget, and keep track of expenses. 

## Getting Started

### Quick Start with Docker

From the **project root** (where this README.md lives), run:

```bash
docker-compose up --build
```

- The **backend** (FastAPI + SQLAlchemy) will be available on port **8000**.
- The **frontend** (Vue) will be available on port **5173**.

Open your browser and navigate to:

> http://localhost:5173

For more in depth information on how to run the files, refer to doc/development.md and doc/running.md

## Existing Features

* Navigation bar

#### Expenses Page
* Manually entering expenses
* Displaying expenses as table and charts/graphs
* Expenses can be put into categories, new categories can be manually added
* Search bars
* Editing function
* Graph toggle feature to switch between Bar and Pie graphs

#### Budget Page
* Budgeting table grouped by category, comparing total expenses in each category to manually entered budget goal
* Automatic comparison between total expenses per category and budget goal with feedback

#### Savings Page
* Manually entered savings plan (amount spend, interest, duration, etc.)
* Automatic calculation of money gained from each savings plan
* Table to keep track of different savings plans
* Editing function
* Search bars

## Todo List
* On savings page, per time period gain, not just total
* On expenses page, a date system that keeps track of different months
* On budget page, a way to keep track of budgets per month in comparison with the dates of the expenses page
