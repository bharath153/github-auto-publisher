# 🚀 GitHub Auto-Publisher

> A desktop GUI application that scans your local projects, generates AI-powered documentation, and publishes everything to GitHub — all in one click.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📁 **Visual Folder Selection** — Browse and select any project folder with a tree view
- 🤖 **AI Documentation** — Automatically generates README.md, CONTRIBUTING.md, and LICENSE
- 🔗 **Multi-LLM Support** — Works with OpenAI, Claude, Kimi, or local Ollama models
- 🚀 **One-Click Publish** — Creates GitHub repo and pushes everything automatically
- 🔒 **Secure** — API keys stored in OS keyring, never hardcoded
- 🖥️ **Cross-Platform** — Works on Windows, macOS, and Linux

## 🎯 Why This Exists

Writing READMEs is tedious. Publishing to GitHub involves multiple terminal commands. 
This tool eliminates both friction points — select your folder, let AI analyze your code 
and generate professional documentation, then publish everything with a single click.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- A GitHub account with a [Personal Access Token](https://github.com/settings/tokens)
- An API key from OpenAI, Claude, or Kimi (or [Ollama](https://ollama.com) for free local AI)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/github-auto-publisher.git
cd github-auto-publisher

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### First Run Setup

1. Click **⚙️ Settings** and configure:
   - Your **GitHub Personal Access Token** (with `repo` scope)
   - Your preferred **AI Provider** and API key
   - Default repository visibility (Public/Private)

2. Click **📁 Browse Folder** and select your project

3. Choose which documents to generate (README, CONTRIBUTING, LICENSE)

4. Click **🚀 Publish to GitHub** and watch the magic happen!

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DESKTOP GUI (PySide6)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ Folder Picker│  │ Settings     │  │ Progress Dashboard  │  │
│  │ (Tree View)  │  │ (API Keys)   │  │ (Logs & Status)     │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  CORE ENGINE (Python)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ File Scanner │  │ Code Analyzer│  │ Doc Generator   │  │
│  │ (os.walk)    │  │ (AST parsing)│  │ (LLM prompts)   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌────────────┐
   │ GitHub   │   │ LLM APIs │   │ File System│
   │ API      │   │(OpenAI/  │   │ (Write     │
   │(PyGithub)│   │Claude/   │   │ generated  │
   │          │   │Kimi)     │   │ docs)      │
   └──────────┘   └──────────┘   └────────────┘
```

## 📁 Project Structure

```
github-auto-publisher/
├── src/
│   ├── main.py                    # Application entry point
│   ├── gui/
│   │   ├── main_window.py         # Main application window
│   │   ├── folder_tree.py         # Folder browser widget
│   │   └── settings_dialog.py     # Configuration dialog
│   ├── core/
│   │   ├── scanner.py             # File system scanner
│   │   └── github_manager.py      # GitHub API operations
│   ├── ai/
│   │   ├── llm_client.py          # Multi-provider LLM client
│   │   ├── prompts.py             # AI prompt templates
│   │   └── document_generator.py  # Documentation generator
│   └── utils/
│       └── config.py              # Configuration manager
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### GitHub Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token (classic) with the `repo` scope
3. Copy and paste into the app's Settings dialog

### AI Providers

| Provider | Setup | Cost |
|----------|-------|------|
| **OpenAI** | Get API key from [platform.openai.com](https://platform.openai.com) | Paid per usage |
| **Claude** | Get API key from [console.anthropic.com](https://console.anthropic.com) | Paid per usage |
| **Kimi** | Get API key from [platform.moonshot.cn](https://platform.moonshot.cn) | Paid per usage |
| **Ollama** | Install from [ollama.com](https://ollama.com), run `ollama run codellama` | **FREE** |

> 💡 **Pro Tip**: Start with Ollama for completely free, private AI. No internet required after model download!

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --windowed --name "GitHubAutoPublisher" src/main.py
```

## 🗺️ Roadmap

- [x] Basic folder scanning and tree view
- [x] README generation with AI
- [x] GitHub repo creation and push
- [x] Multi-LLM provider support
- [ ] Smart file sampling for large repos
- [ ] CONTRIBUTING.md and LICENSE generation
- [ ] Template system for custom documentation
- [ ] Drag-and-drop folder support
- [ ] Auto-detect project type (Python, Node, Rust, etc.)
- [ ] CI/CD template generation
- [ ] Screenshot/demo GIF auto-generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PySide6](https://wiki.qt.io/Qt_for_Python) for the GUI
- GitHub integration via [PyGithub](https://github.com/PyGithub/PyGithub)
- AI powered by OpenAI, Anthropic, Moonshot AI, or local Ollama models
