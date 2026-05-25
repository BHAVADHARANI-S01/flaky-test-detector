# Flaky Test Detector 🚦

AI-powered flaky test detection tool for CI/CD pipelines and automated testing workflows.

![GitHub stars](https://img.shields.io/github/stars/BHAVADHARANI-S01/flaky-test-detector?style=social)
![GitHub forks](https://img.shields.io/github/forks/BHAVADHARANI-S01/flaky-test-detector?style=social)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

Flaky tests are tests that randomly pass or fail without code changes.  
They reduce trust in CI/CD pipelines and waste developer time.

**Flaky Test Detector** helps identify unstable tests automatically by analyzing repeated test execution patterns.

---

## ✨ Features

- Detects flaky tests automatically
- Generates detailed test stability reports
- CI/CD friendly
- Lightweight and easy to integrate
- Supports automated test workflows
- Helps improve build reliability

---

## 🛠️ Tech Stack

- Python
- PyTest
- CI/CD Integration
- GitHub Actions

---

## 📂 Project Structure

```bash
flaky-test-detector/
│── detector/
│── tests/
│── reports/
│── requirements.txt
│── README.md
```

---

## ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/BHAVADHARANI-S01/flaky-test-detector.git
```

Move into the project folder:

```bash
cd flaky-test-detector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the detector:

```bash
python main.py
```

Example output:

```bash
Analyzing test executions...

⚠️ Flaky Test Detected:
test_login.py::test_authentication

Failure Rate: 37%
Status: Unstable
```

---

## 📊 Why This Project Matters

Flaky tests can:
- Slow down deployments
- Cause false CI failures
- Waste debugging time
- Reduce confidence in automated testing

This project aims to improve software quality by identifying unreliable tests early.

---

## 🚀 Future Improvements

- Machine learning-based prediction
- Dashboard visualization
- Multi-framework support
- Real-time CI analytics
- GitHub Actions plugin

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## 🌟 Support

If you found this project useful, consider giving it a ⭐ on GitHub.

GitHub Repo:  
https://github.com/BHAVADHARANI-S01/flaky-test-detector

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed by **BHAVA DHARANI**
