# Contributing to Django Gotify

First off, thank you for considering contributing to `django-gotify`! It’s people like you who make the open-source community such a great place to learn, inspire, and create.

## 🛠 Development Setup

To set up a local development environment:

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
```bash
git clone [https://github.com/your-username/django-gotify.git](https://github.com/your-username/django-gotify.git)
cd django-gotify
```

3. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


4. **Install dependencies**:
```bash
pip install -e .
pip install django gotify
```



## 🧪 Running Tests

Before submitting a Pull Request, please ensure all tests pass. We use a custom test runner to simulate the Django environment.

To run the test suite:

```bash
python runtests.py
```

Your code should ideally maintain or increase test coverage. If you add a new feature, please add a corresponding test in the `tests/` directory.

## 📝 Submitting Changes

1. **Create a new branch** for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
```


2. **Commit your changes** with descriptive commit messages.
3. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```


4. **Open a Pull Request** against the `main` branch of the original repository.

## 📜 Code Style

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
* Ensure your code is compatible with the Python and Django versions listed in `pyproject.toml`.
* Add docstrings to new classes and methods.

## ❓ Questions?

If you have any questions or need help with the setup, feel free to open an Issue in the repository.
