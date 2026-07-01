# 🛠️ Setup Guide — GitHub Auto-Publisher

Follow these steps to get the project running on your machine.

---

## Step 1: Create Your GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name it `github-auto-publisher`
3. Make it **Public** (or Private if you prefer)
4. **DO NOT** initialize with README (we'll push our own)
5. Click **Create repository**

---

## Step 2: Clone & Setup Locally

```bash
# Clone your new repo
git clone https://github.com/YOUR_USERNAME/github-auto-publisher.git
cd github-auto-publisher

# Create the project structure
mkdir -p src/{gui,core,ai,utils}
mkdir -p tests assets/icons

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

---

## Step 3: Copy All Source Files

Copy all the generated `.py` files into their correct locations:

```
github-auto-publisher/
├── src/
│   ├── main.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── folder_tree.py
│   │   └── settings_dialog.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── scanner.py
│   │   └── github_manager.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   ├── prompts.py
│   │   └── document_generator.py
│   └── utils/
│       ├── __init__.py
│       └── config.py
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

Create empty `__init__.py` files:
```bash
touch src/gui/__init__.py
touch src/core/__init__.py
touch src/ai/__init__.py
touch src/utils/__init__.py
```

---

## Step 4: Get Your API Keys

### GitHub Token (REQUIRED)
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Check the **`repo`** scope (full control of private repositories)
4. Generate and **copy the token immediately**

### OpenAI API Key (if using OpenAI)
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy it

### Claude API Key (if using Claude)
1. Go to [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Create new key
3. Copy it

### Ollama (FREE alternative — Recommended for testing)
1. Download from [ollama.com](https://ollama.com)
2. Install and run: `ollama run codellama`
3. No API key needed! The app will connect to `http://localhost:11434`

---

## Step 5: Run the Application

```bash
# Make sure you're in the project root and venv is activated
python src/main.py
```

The GUI should open. Now:
1. Click **⚙️ Settings**
2. Paste your GitHub token
3. Select your AI provider and paste the API key
4. Click **Save Settings**
5. Click **📁 Browse Folder** and select a test project
6. Check which documents you want generated
7. Click **🚀 Publish to GitHub**

---

## Step 6: Build & Package (Optional)

To create a standalone executable:

```bash
pip install pyinstaller

# Windows
pyinstaller --onefile --windowed --name "GitHubAutoPublisher" --icon=assets/icon.ico src/main.py

# macOS
pyinstaller --onefile --windowed --name "GitHubAutoPublisher" --icon=assets/icon.icns src/main.py

# Linux
pyinstaller --onefile --windowed --name "github-auto-publisher" src/main.py
```

The executable will be in the `dist/` folder.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Make sure venv is activated: `source venv/bin/activate` |
| GitHub auth fails | Check your token has `repo` scope and hasn't expired |
| LLM API errors | Verify your API key is correct and you have credits |
| Ollama connection refused | Make sure Ollama is running: `ollama serve` |
| GUI looks weird | Update PySide6: `pip install --upgrade PySide6` |

---

## 🎉 You're All Set!

Now you can:
- Select any project folder from your PC
- Let AI analyze and document it
- Publish to GitHub with one click

**Pro tip**: Test with a small project first (like a simple Python script folder) before trying large codebases.
