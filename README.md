# ⚡ Copilot Monitor

> Real-time AI-based evaluator for code suggestions using Gemini + Supabase + VS Code Extension

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Made with TypeScript](https://img.shields.io/badge/language-TypeScript-blue)
![Built with Flask](https://img.shields.io/badge/backend-Flask-red)
![VS Code Extension](https://img.shields.io/badge/editor-VSCode-purple)

---

## 🚀 Overview

Copilot Monitor is a developer tool that **captures code suggestions inside VS Code**, sends them to a **Gemini-powered AI model** for evaluation, and logs results in **Supabase**.  
It displays a live rating notification inside your editor and stores prompt history for feedback & analysis.

---

## 🧱 Tech Stack

| Layer     | Tech                      |
|-----------|---------------------------|
| Frontend  | VS Code Extension (TypeScript) |
| Backend   | Flask + Gemini API        |
| Database  | Supabase (PostgreSQL)     |
| Model     | Gemini 1.5 Flash          |

---

## ⚙️ Features

- 🧠 AI-based scoring of code completions (1–10 scale)
- 🔁 Real-time interaction between VS Code, backend, and Supabase
- 💡 Live popup notifications inside your editor
- 📦 Prompt logging & analytics via Supabase
- 🔁 Retry logic & user acceptance tracking (planned)

---

## 📦 Installation & Setup

### 🔧 Backend (Flask + Gemini + Supabase)

```bash
git clone https://github.com/your-username/copilot-monitor-backend.git
cd copilot-monitor-backend
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt

