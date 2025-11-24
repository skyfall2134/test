# Saucedemo Login Autotests

Pytest + Selenium UI checks for https://www.saucedemo.com.

## Setup

1. Create / activate a virtualenv (PyCharm can do this automatically).
2. Install deps: `pip install -r requirements.txt`.
3. Ensure Google Chrome and matching ChromeDriver are available on PATH.

## Running

Execute all tests:

```
pytest -v
```

Set `--headed` by commenting out `--headless=new` in `tests/test_saucedemo_login.py` if you want to see the browser.

