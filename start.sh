#!/bin/bash

echo "✅ Virtual muhit yaratilyapti..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Kutubxonalar o'rnatilyapti..."
pip install -r requirements.txt

echo "🚀 Bot ishga tushyapti..."
python bot.py
