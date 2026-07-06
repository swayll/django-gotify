---
name: Bug report
about: Create a report to help improve django-gotify
title: "[Bug] "
labels: bug
assignees: ""

---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:

1. Configure `settings.py` with:
   ```python
   GOTIFY_URL = "..."
   GOTIFY_TOKEN = "..."
   ```
2. Call `send_mail(...)` / trigger a log statement
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- Python version: `3.x`
- Django version: `4.x / 5.x`
- django-gotify version: `0.x`
- Gotify server version: `...`

**Traceback (if applicable)**
```
paste traceback here
```
