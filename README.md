# 🔗 uTrace – Advanced URL Redirect & SSL Checker

`uTrace.py` is a terminal-based Python tool that helps you inspect how a given URL behaves when accessed. It checks if a website redirects to another, how many times it redirects, what the final destination is, whether it's using HTTPS, and whether the SSL certificate is valid. It also prints response time and key technical details. This is useful for developers, testers, or anyone interested in network diagnostics and security.

---

## 🎯 Features

- 🔍 Parses and displays full URL structure
- 🔁 Shows full redirect history (with HTTP status and timing)
- 🔒 Verifies if HTTPS is used
- 🛡️ Checks SSL certificate validity and expiry date
- ⏱️ Displays final response time
- 📄 Supports both single and batch URL checking from a `.txt` file
- 🎨 Color-coded and styled output using `colorama`

---

## 📦 Requirements

- Python 3.6 or later
- Required libraries:
```bash
  pip install requests colorama
```

---

## 🚀 How to Run

### ▶️ Single URL Mode

```bash
python uTrace.py
```
When prompted:
```
Select an option (1/2/3): 1
Enter a URL: http://example.com
```

---

### 📁 Batch URL Mode

Prepare a text file (e.g., `urls.txt`) with one URL per line:

```
http://bit.ly/3GTL3vV
http://t.co
http://github.com
```

Then run:

```bash
python uTrace.py
```
Select:
```
Select an option (1/2/3): 2
Enter path to file with URLs: urls.txt
```

---

### 🆘 Help Menu

To view description and usage:

```
Select an option (1/2/3): 3
```

---

## 📄 Example Output

```
URL: http://github.com
📎 Domain: github.com
🔗 Scheme: https
📁 Path: /
🔍 Final URL: https://github.com
🔒 HTTPS: Yes
🛡️ SSL Certificate valid (expires 2025-06-30)

🔁 Redirected 1 times:
 1. 301 → https://github.com (0.145s)

⏱️ Final response time: 0.142s
```

---

## 📁 Files

- `uTrace.py` → main script
- `urls.txt` → (optional) list of URLs for batch mode

---

## 👨‍💻 Author

Coded by **Abinav S**  

---

## 📄 License

Free to use for educational and testing purposes. No warranty or guarantees.
