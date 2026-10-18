# Sauce Demo UI test automation

![tests](https://github.com/eithemshashank/qa-automation-saucedemo/actions/workflows/tests.yml/badge.svg)

Automated browser tests for the login, product list, cart and checkout of [Sauce Demo](https://www.saucedemo.com), a public practice shop made for testers. Built with Python, pytest and Playwright, using the page-object pattern. The suite found two real bugs, written up in `docs/bug_reports/`.

## What is covered

19 test cases (see [`docs/test_plan.md`](docs/test_plan.md)):

| Area | Tests |
|---|---|
| Smoke | login page loads |
| Login | valid login, locked-out user, wrong password, empty username, empty password |
| Products | 6 products listed, sort by price, sort by name |
| Cart | badge count up and down, cart contents |
| Checkout | full order, order total, three required-field errors |
| Known bugs | 2 tests that fail on purpose because of confirmed bugs |

**Result:** 17 pass, 2 are expected failures (`xfail`) for the bugs below.

## Bugs found

| ID | Summary | Severity |
|---|---|---|
| [BUG-001](docs/bug_reports/BUG-001.md) | `problem_user` sees the same placeholder image for all 6 products | Minor |
| [BUG-002](docs/bug_reports/BUG-002.md) | Sorting has no effect for `problem_user` | Major |

`problem_user` is a deliberately faulty demo account, so these bugs are expected on this site. They show the approach: reproduce, capture evidence, write a clear report, and keep an automated test that will tell us when it is fixed.

## Project layout

```
pages/        page objects: where each page's elements and actions live
tests/        test files, one per area
conftest.py   shared setup (logged-in browser, login as any user)
docs/         test plan and bug reports
.github/      GitHub Actions workflow that runs the tests on every push
```

## Run it

```
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest
```

Add `--headed` to watch the browser. An HTML report is written to `reports/report.html`.

## Limitations

- Chromium only; no mobile or cross-browser runs.
- Tests run against a live public website, so a site outage or change can fail them.
- UI tests only: no API, performance or security testing.
