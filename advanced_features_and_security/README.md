# LibraryProject Security Enhancements

This document details the security measures implemented in this Django project, based on Step 5 of the security task.

## 1. Secure Settings (`LibraryProject/settings.py`)

Several settings were configured to harden the application in a production environment.

* `DEBUG = False`: Turned off debug mode to prevent leaking sensitive information.
* `ALLOWED_HOSTS`: Configured to only allow requests from specific domains.
* `SESSION_COOKIE_SECURE = True`: Enforces that session cookies are only sent over HTTPS.
* `CSRF_COOKIE_SECURE = True`: Enforces that the CSRF cookie is only sent over HTTPS.
* `X_FRAME_OPTIONS = 'SAMEORIGIN'`: Protects against clickjacking by preventing the site from being rendered in a frame on another domain.
* `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents the browser from "MIME-sniffing" (guessing) content types, which mitigates XSS.
* `SECURE_BROWSER_XSS_FILTER = True`: Enables a legacy XSS filter in older browsers.

## 2. Content Security Policy (CSP)

To mitigate Cross-Site Scripting (XSS), `django-csp` was implemented.

* **Middleware:** `csp.middleware.CSPMiddleware` was added to `MIDDLEWARE`.
* **Policy:** `CSP_DEFAULT_SRC = ("'self'",)` was set as a baseline, allowing content (scripts, styles, etc.) to be loaded only from our own domain. This blocks all inline scripts and resources from untrusted CDNs by default.

## 3. CSRF Protection (Templates)

All forms that submit via `POST` have been secured against Cross-Site Request Forgery.

* **Implementation:** The `{% csrf_token %}` tag was added to all relevant form templates (e.g., `bookshelf/form_example.html`).
* **Function:** This tag renders a hidden input with a unique token, which Django's `CsrfViewMiddleware` validates upon submission.

## 4. SQL Injection Prevention (`bookshelf/views.py`)

All database queries have been written securely to prevent SQL injection.

* **Method:** Instead of using raw SQL with string formatting (which is highly insecure), all database lookups use the **Django ORM** (e.g., `Book.objects.filter(title__icontains=query)`).
* **Why it's Secure:** The ORM uses parameterized queries, which means user input is always treated as data, not as executable SQL code.

## 5. Input Validation & Sanitization (`bookshelf/forms.py`)

All user input is now validated and sanitized before use.

* **Method:** A `SearchForm` was created in `bookshelf/forms.py`.
* **Validation:** The view checks `form.is_valid()` before using the data.
* **Sanitization:** The form's `clean_query` method uses `bleach.clean()` to strip any potentially malicious HTML tags from the user's input before it is ever used, preventing XSS if that query is rendered back to the page.