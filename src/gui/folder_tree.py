"""Folder tree widget for project selection."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QTreeWidget, QTreeWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from pathlib import Path


class FolderTreeWidget(QWidget):
    """Widget for selecting and displaying project folder structure."""

    folder_selected = Signal(str)  # Emits folder path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_path = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Header with browse button
        header = QHBoxLayout()
        self.path_label = QLabel("No folder selected")
        self.path_label.setStyleSheet("color: #666; font-style: italic;")
        self.path_label.setWordWrap(True)

        self.browse_btn = QPushButton("📁 Browse Folder")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ea44f;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c974b;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_folder)

        header.addWidget(self.path_label, stretch=1)
        header.addWidget(self.browse_btn)
        layout.addLayout(header)

        # Tree widget for folder structure
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Type", "Size"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 80)
        self.tree.setColumnWidth(2, 80)
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 4px;
                background: #f6f8fa;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #ddf4ff;
                color: #0969da;
            }
        """)
        layout.addWidget(self.tree)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #57606a; font-size: 12px;")
        layout.addWidget(self.info_label)

    def browse_folder(self):
        """Open folder dialog and load structure."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder",
            str(Path.home()),
            QFileDialog.ShowDirsOnly
        )
        if folder:
            self.load_folder(folder)

    def load_folder(self, path: str):
        """Load and display folder structure."""
        self.selected_path = path
        self.path_label.setText(f"Selected: {path}")
        self.path_label.setStyleSheet("color: #0969da; font-weight: bold;")

        self.tree.clear()
        root_item = QTreeWidgetItem(self.tree)
        root_item.setText(0, Path(path).name)
        root_item.setText(1, "Folder")
        root_item.setIcon(0, self.style().standardIcon(self.style().SP_DirIcon))

        self._populate_tree(path, root_item)
        root_item.setExpanded(True)

        self.folder_selected.emit(path)
        self.info_label.setText(f"Folder loaded. Expand items to view contents.")

    def _populate_tree(self, path: str, parent_item: QTreeWidgetItem, depth: int = 0):
        """Recursively populate tree with folder contents."""
        if depth > 3:  # Limit depth for performance
            return

        try:
            entries = sorted(Path(path).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

            # Skip hidden and common ignore directories
            skip_dirs = {".git", "__pycache__", "node_modules", "venv", ".venv", "dist", "build"}

            for entry in entries[:100]:  # Limit items per directory
                if entry.name.startswith(".") and entry.name != ".gitignore":
                    continue
                if entry.is_dir() and entry.name in skip_dirs:
                    continue

                item = QTreeWidgetItem(parent_item)
                item.setText(0, entry.name)

                if entry.is_dir():
                    item.setText(1, "Folder")
                    item.setIcon(0, self.style().standardIcon(self.style().SP_DirIcon))
                    if depth < 2:
                        self._populate_tree(str(entry), item, depth + 1)
                else:
                    item.setText(1, "File")
                    size = entry.stat().st_size
                    item.setText(2, self._format_size(size))
                    item.setIcon(0, self.style().standardIcon(self.style().SP_FileIcon))

        except PermissionError:
            pass

    def _format_size(self, size: int) -> str:
        """Format file size for display."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
