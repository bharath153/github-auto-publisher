"""Main application window."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit,
    QCheckBox, QLineEdit, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt, QThread, Signal
import sys
sys.path.insert(0, "src")

from gui.folder_tree import FolderTreeWidget
from gui.settings_dialog import SettingsDialog
from core.scanner import ProjectScanner
from core.github_manager import GitHubManager
from ai.llm_client import LLMClient, LLMProvider
from ai.document_generator import DocumentGenerator
from utils.config import Config


class PublishWorker(QThread):
    """Background worker for the publish process."""
    progress = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, folder_path: str, repo_name: str, options: dict, config: Config):
        super().__init__()
        self.folder_path = folder_path
        self.repo_name = repo_name
        self.options = options
        self.config = config

    def run(self):
        try:
            # Step 1: Scan project
            self.progress.emit("🔍 Scanning project structure...")
            scanner = ProjectScanner(self.folder_path)
            scan_result = scanner.scan()
            self.progress.emit(f"✅ Found {scan_result['total_files']} files ({scan_result['total_size_mb']} MB)")

            # Step 2: Generate context for LLM
            self.progress.emit("🧠 Analyzing codebase with AI...")
            context = scanner.get_context_for_llm()

            # Step 3: Initialize LLM
            provider_str = self.config.get("llm_provider", "openai")
            provider = LLMProvider(provider_str)

            api_key = ""
            if provider == LLMProvider.OPENAI:
                api_key = self.config.get("openai_api_key", "")
            elif provider == LLMProvider.CLAUDE:
                api_key = self.config.get("claude_api_key", "")
            elif provider == LLMProvider.KIMI:
                api_key = self.config.get("kimi_api_key", "")

            kwargs = {}
            if provider == LLMProvider.OLLAMA:
                kwargs["base_url"] = self.config.get("ollama_url", "http://localhost:11434")
                kwargs["model"] = self.config.get("ollama_model", "codellama")

            if provider != LLMProvider.OLLAMA and not api_key:
                self.finished_signal.emit(False, "❌ API key not configured. Go to Settings.")
                return

            llm = LLMClient(provider, api_key, **kwargs)
            doc_gen = DocumentGenerator(llm)

            # Step 4: Generate documents
            self.progress.emit("📝 Generating documentation with AI...")
            docs = doc_gen.generate_all(context, self.options)

            for doc_name in docs.keys():
                self.progress.emit(f"   ✓ Generated {doc_name}")

            llm.close()

            # Step 5: Create GitHub repo
            self.progress.emit("🚀 Creating GitHub repository...")
            github = GitHubManager(self.config.get("github_token", ""))

            visibility = self.config.get("default_visibility", "public") == "private"
            clone_url = github.create_repository(
                name=self.repo_name,
                description=f"Auto-published project: {scan_result['project_name']}",
                private=visibility
            )

            self.progress.emit(f"✅ Repository created: {clone_url}")

            # Step 6: Push to GitHub
            self.progress.emit("📤 Pushing files to GitHub...")
            github.push_local_project(
                local_path=self.folder_path,
                repo_url=clone_url,
                commit_message="Initial commit with AI-generated documentation",
                generated_files=docs
            )

            self.progress.emit("🎉 Project published successfully!")
            self.finished_signal.emit(True, f"Published to: {clone_url}")

        except Exception as e:
            self.finished_signal.emit(False, f"❌ Error: {str(e)}")


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 GitHub Auto-Publisher")
        self.setMinimumSize(900, 700)
        self.config = Config()
        self.worker = None
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("🚀 GitHub Auto-Publisher")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #24292f;
            padding: 10px 0;
        """)
        layout.addWidget(header)

        subtitle = QLabel("Select a project folder → AI generates docs → Publish to GitHub")
        subtitle.setStyleSheet("color: #57606a; font-size: 13px; padding-bottom: 10px;")
        layout.addWidget(subtitle)

        # Main splitter
        splitter = QSplitter(Qt.Vertical)

        # Top: Folder picker
        self.folder_tree = FolderTreeWidget()
        self.folder_tree.folder_selected.connect(self.on_folder_selected)
        splitter.addWidget(self.folder_tree)

        # Bottom: Options and controls
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Repository name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Repository Name:"))
        self.repo_name = QLineEdit()
        self.repo_name.setPlaceholderText("my-awesome-project")
        name_layout.addWidget(self.repo_name)
        bottom_layout.addLayout(name_layout)

        # Document options
        options_label = QLabel("📄 Documents to Generate:")
        options_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        bottom_layout.addWidget(options_label)

        options_layout = QHBoxLayout()
        self.gen_readme = QCheckBox("README.md")
        self.gen_readme.setChecked(True)
        self.gen_contributing = QCheckBox("CONTRIBUTING.md")
        self.gen_license = QCheckBox("LICENSE (MIT)")
        options_layout.addWidget(self.gen_readme)
        options_layout.addWidget(self.gen_contributing)
        options_layout.addWidget(self.gen_license)
        options_layout.addStretch()
        bottom_layout.addLayout(options_layout)

        # Action buttons
        btn_layout = QHBoxLayout()

        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.clicked.connect(self.open_settings)

        self.publish_btn = QPushButton("🚀 Publish to GitHub")
        self.publish_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ea44f;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2c974b; }
            QPushButton:disabled {
                background-color: #94d3a2;
                color: #fff;
            }
        """)
        self.publish_btn.clicked.connect(self.start_publish)
        self.publish_btn.setEnabled(False)

        btn_layout.addWidget(self.settings_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.publish_btn)
        bottom_layout.addLayout(btn_layout)

        # Progress area
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #0969da;
                border-radius: 6px;
            }
        """)
        bottom_layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Progress logs will appear here...")
        self.log_output.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 8px;
                background: #f6f8fa;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        self.log_output.setMaximumHeight(150)
        bottom_layout.addWidget(self.log_output)

        splitter.addWidget(bottom_widget)
        splitter.setSizes([400, 300])
        layout.addWidget(splitter)

    def on_folder_selected(self, path: str):
        """Handle folder selection."""
        self.selected_folder = path
        self.repo_name.setText(Path(path).name.lower().replace(" ", "-"))
        self.publish_btn.setEnabled(True)
        self.log("📁 Folder selected: " + path)

    def open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self)
        dialog.exec()

    def log(self, message: str):
        """Add log message."""
        self.log_output.append(message)

    def start_publish(self):
        """Start the publish process."""
        if not hasattr(self, 'selected_folder') or not self.selected_folder:
            QMessageBox.warning(self, "Error", "Please select a folder first!")
            return

        repo_name = self.repo_name.text().strip()
        if not repo_name:
            QMessageBox.warning(self, "Error", "Please enter a repository name!")
            return

        # Check GitHub token
        if not self.config.get("github_token"):
            QMessageBox.warning(self, "Error", "Please configure your GitHub token in Settings!")
            return

        # Confirm
        reply = QMessageBox.question(
            self,
            "Confirm Publish",
            f"Create GitHub repository '\u003c{repo_name}\u003e' and push all files?

"
            f"This will:
"
            f"  • Scan {Path(self.selected_folder).name}
"
            f"  • Generate AI documentation
"
            f"  • Create GitHub repo
"
            f"  • Push all files

"
            f"Continue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Start worker
        self.publish_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.log_output.clear()

        options = {
            "readme": self.gen_readme.isChecked(),
            "contributing": self.gen_contributing.isChecked(),
            "license": self.gen_license.isChecked(),
            "license_type": "mit",
        }

        self.worker = PublishWorker(self.selected_folder, repo_name, options, self.config)
        self.worker.progress.connect(self.log)
        self.worker.finished_signal.connect(self.on_publish_finished)
        self.worker.start()

    def on_publish_finished(self, success: bool, message: str):
        """Handle publish completion."""
        self.progress_bar.setVisible(False)
        self.publish_btn.setEnabled(True)
        self.log(message)

        if success:
            QMessageBox.information(self, "Success!", message)
        else:
            QMessageBox.critical(self, "Error", message)
