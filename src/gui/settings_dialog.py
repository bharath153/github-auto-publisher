"""Settings dialog for API configuration."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QGroupBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
import sys
sys.path.insert(0, "src")
from utils.config import Config


class SettingsDialog(QDialog):
    """Dialog for configuring API keys and preferences."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.setWindowTitle("⚙️ Settings")
        self.setMinimumWidth(500)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # GitHub Settings
        github_group = QGroupBox("GitHub Configuration")
        github_layout = QFormLayout()

        self.github_token = QLineEdit()
        self.github_token.setEchoMode(QLineEdit.Password)
        self.github_token.setPlaceholderText("ghp_xxxxxxxxxxxx")
        github_layout.addRow("GitHub Token:", self.github_token)

        self.visibility = QComboBox()
        self.visibility.addItems(["Public", "Private"])
        github_layout.addRow("Default Visibility:", self.visibility)

        github_group.setLayout(github_layout)
        layout.addWidget(github_group)

        # LLM Provider Settings
        llm_group = QGroupBox("AI Provider Configuration")
        llm_layout = QFormLayout()

        self.provider = QComboBox()
        self.provider.addItems(["OpenAI", "Claude", "Kimi", "Ollama (Local)"])
        self.provider.currentTextChanged.connect(self.on_provider_changed)
        llm_layout.addRow("LLM Provider:", self.provider)

        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.Password)
        self.api_key.setPlaceholderText("sk-xxxxxxxx")
        llm_layout.addRow("API Key:", self.api_key)

        self.ollama_url = QLineEdit()
        self.ollama_url.setPlaceholderText("http://localhost:11434")
        self.ollama_url.setVisible(False)
        llm_layout.addRow("Ollama URL:", self.ollama_url)

        self.ollama_model = QLineEdit()
        self.ollama_model.setPlaceholderText("codellama")
        self.ollama_model.setVisible(False)
        llm_layout.addRow("Ollama Model:", self.ollama_model)

        llm_group.setLayout(llm_layout)
        layout.addWidget(llm_group)

        # Info label
        info = QLabel(
            "💡 <b>Tip:</b> Get your GitHub token from "
            "<a href='https://github.com/settings/tokens'>GitHub Settings → Developer settings → Personal access tokens</a><br>"
            "For Ollama, install it from <a href='https://ollama.com'>ollama.com</a> and run models locally for free!"
        )
        info.setOpenExternalLinks(True)
        info.setWordWrap(True)
        info.setStyleSheet("color: #57606a; font-size: 11px; padding: 8px;")
        layout.addWidget(info)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ea44f;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2c974b; }
        """)
        self.save_btn.clicked.connect(self.save_settings)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def on_provider_changed(self, text: str):
        """Show/hide fields based on provider selection."""
        is_ollama = text == "Ollama (Local)"
        self.api_key.setVisible(not is_ollama)
        self.ollama_url.setVisible(is_ollama)
        self.ollama_model.setVisible(is_ollama)

    def load_settings(self):
        """Load existing settings."""
        self.github_token.setText(self.config.get("github_token", ""))

        visibility = self.config.get("default_visibility", "public")
        self.visibility.setCurrentIndex(0 if visibility == "public" else 1)

        provider = self.config.get("llm_provider", "openai")
        provider_map = {"openai": 0, "claude": 1, "kimi": 2, "ollama": 3}
        self.provider.setCurrentIndex(provider_map.get(provider, 0))

        # Load the appropriate API key based on provider
        current_provider = self.provider.currentText().lower().replace(" (local)", "")
        if current_provider == "openai":
            self.api_key.setText(self.config.get("openai_api_key", ""))
        elif current_provider == "claude":
            self.api_key.setText(self.config.get("claude_api_key", ""))
        elif current_provider == "kimi":
            self.api_key.setText(self.config.get("kimi_api_key", ""))

        self.ollama_url.setText(self.config.get("ollama_url", "http://localhost:11434"))
        self.ollama_model.setText(self.config.get("ollama_model", "codellama"))

    def save_settings(self):
        """Save settings to config."""
        provider_text = self.provider.currentText().lower().replace(" (local)", "")

        self.config.set("github_token", self.github_token.text())
        self.config.set("default_visibility", "public" if self.visibility.currentIndex() == 0 else "private")
        self.config.set("llm_provider", provider_text)

        # Save provider-specific keys
        if provider_text == "openai":
            self.config.set("openai_api_key", self.api_key.text())
        elif provider_text == "claude":
            self.config.set("claude_api_key", self.api_key.text())
        elif provider_text == "kimi":
            self.config.set("kimi_api_key", self.api_key.text())
        elif provider_text == "ollama":
            self.config.set("ollama_url", self.ollama_url.text())
            self.config.set("ollama_model", self.ollama_model.text())

        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.accept()
