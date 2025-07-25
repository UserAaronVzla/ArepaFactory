# ArepaFactory — Mini Web Challenge

Two-page Flask app that lets you add arepa products (name, price) and search them.

## About

* **SQL** database (`sqlite3`) with parameterised queries
* Manual security headers (CSP, X-Frame-Options …)
* Session-based CSRF token
* Runs on Debian/Ubuntu with Python 3.11+

## Prerequisites
```bash
sudo apt -y install python3 python3-venv python3-pip git
```
## Setup
1. Clone the repository
```bash
git clone https://github.com/UserAaronVzla/ArepaFactory.git
```
2. Move yourself inside the folder
```bash
cd ArepaFactory
```
3. Create and activate a virtual environment where the app will run
```bash
python3 -m venv ArepaFactory-venv && source ArepaFactory-venv/bin/activate
```
4. Prepare the virtual environment by installing the application requirements
```bash
pip install -r requirements.txt
```
5. Run the SQLite database
```bash
python init_db.py
```
6. Turn on the "Arepa Factory" application
```bash
python ArepaFactory_App.py
```
7. Browse to
```
http://127.0.0.1:5000/add
```
>**Note:** You can use your VM IP address instead of "127.0.0.1" in case you want to test the application from an attacker machine
