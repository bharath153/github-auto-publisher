"""File system scanner for project analysis."""
import os
from pathlib import Path
from typing import List, Dict, Any


class ProjectScanner:
    """Scans a project folder and extracts relevant information."""

    # Files to always skip
    SKIP_DIRS = {
        ".git", "__pycache__", "node_modules", ".venv", "venv",
        "env", "dist", "build", ".idea", ".vscode", "target",
        ".pytest_cache", ".mypy_cache", "*.egg-info"
    }

    # Binary extensions to skip content reading
    BINARY_EXTENSIONS = {
        ".exe", ".dll", ".so", ".dylib", ".bin", ".dat",
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico",
        ".mp3", ".mp4", ".avi", ".mov", ".wav",
        ".zip", ".tar", ".gz", ".rar", ".7z",
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".db", ".sqlite", ".sqlite3"
    }

    # Key files that provide project context
    KEY_FILES = [
        "package.json", "requirements.txt", "Cargo.toml",
        "pom.xml", "build.gradle", "go.mod", "composer.json",
        "Gemfile", "setup.py", "pyproject.toml", "Makefile",
        "Dockerfile", "docker-compose.yml", ".github/workflows"
    ]

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.files: List[Dict[str, Any]] = []
        self.structure: Dict[str, Any] = {}
        self.total_size = 0
        self.file_count = 0

    def scan(self) -> Dict[str, Any]:
        """Scan the project folder and return analysis."""
        self.files = []
        self.structure = {"name": self.project_path.name, "type": "directory", "children": []}

        for root, dirs, files in os.walk(self.project_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS and not d.startswith(".")]

            rel_root = Path(root).relative_to(self.project_path)
            current_dir = self._get_or_create_dir(rel_root)

            for file in files:
                if file.startswith(".") and file != ".gitignore":
                    continue

                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.project_path)

                try:
                    stat = file_path.stat()
                    size = stat.st_size
                    self.total_size += size
                    self.file_count += 1

                    is_binary = file_path.suffix.lower() in self.BINARY_EXTENSIONS
                    is_key = file in self.KEY_FILES or any(file.endswith(k) for k in self.KEY_FILES)

                    file_info = {
                        "name": file,
                        "path": str(rel_path),
                        "full_path": str(file_path),
                        "size": size,
                        "extension": file_path.suffix.lower(),
                        "is_binary": is_binary,
                        "is_key": is_key,
                    }

                    # Read content for text files (with size limit)
                    if not is_binary and size < 100_000:  # 100KB limit
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                file_info["content_preview"] = f.read(2000)
                        except Exception:
                            file_info["content_preview"] = "[Could not read file]"

                    self.files.append(file_info)
                    current_dir["children"].append({
                        "name": file,
                        "type": "file",
                        "size": size,
                        "is_key": is_key
                    })

                except (OSError, PermissionError):
                    continue

        return {
            "project_name": self.project_path.name,
            "total_files": self.file_count,
            "total_size_mb": round(self.total_size / (1024 * 1024), 2),
            "structure": self.structure,
            "files": self.files,
            "key_files": [f for f in self.files if f["is_key"]],
            "languages": self._detect_languages(),
        }

    def _get_or_create_dir(self, rel_path: Path) -> Dict:
        """Get or create directory entry in structure tree."""
        if str(rel_path) == ".":
            return self.structure

        current = self.structure
        for part in rel_path.parts:
            found = None
            for child in current.get("children", []):
                if child.get("name") == part and child.get("type") == "directory":
                    found = child
                    break
            if not found:
                found = {"name": part, "type": "directory", "children": []}
                current.setdefault("children", []).append(found)
            current = found
        return current

    def _detect_languages(self) -> List[str]:
        """Detect primary programming languages in project."""
        ext_counts = {}
        for f in self.files:
            ext = f["extension"]
            if ext:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1

        lang_map = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".jsx": "React", ".tsx": "React/TS", ".java": "Java",
            ".cpp": "C++", ".c": "C", ".go": "Go", ".rs": "Rust",
            ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
            ".kt": "Kotlin", ".scala": "Scala", ".r": "R",
            ".html": "HTML", ".css": "CSS", ".scss": "SCSS",
            ".vue": "Vue", ".svelte": "Svelte"
        }

        languages = []
        for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1])[:5]:
            if ext in lang_map:
                languages.append(f"{lang_map[ext]} ({count} files)")

        return languages

    def get_context_for_llm(self, max_files: int = 20) -> str:
        """Generate a condensed project summary for LLM consumption."""
        key_files = [f for f in self.files if f.get("is_key")]
        code_files = [f for f in self.files if not f.get("is_binary") and f.get("extension")]

        # Sort by importance: key files first, then by size (smaller = more likely config/important)
        important_files = sorted(key_files, key=lambda x: x["size"])[:10]
        sample_code = sorted(code_files, key=lambda x: x["size"])[:max_files]

        context_parts = [
            f"# Project: {self.project_path.name}",
            f"## Structure
",
            self._format_tree(self.structure),
            f"
## Key Files
"
        ]

        for f in important_files:
            content = f.get("content_preview", "")
            if content:
                context_parts.append(f"### {f['path']}
```
{content[:1500]}
```
")

        context_parts.append("## Code Samples
")
        for f in sample_code[:10]:
            content = f.get("content_preview", "")
            if content and len(content) > 50:
                context_parts.append(f"### {f['path']}
```{f['extension'][1:]}
{content[:1000]}
```
")

        return "
".join(context_parts)

    def _format_tree(self, node: Dict, prefix: str = "") -> str:
        """Format directory tree as string."""
        lines = []
        children = node.get("children", [])
        dirs = [c for c in children if c.get("type") == "directory"]
        files = [c for c in children if c.get("type") == "file"]

        for d in dirs:
            lines.append(f"{prefix}📁 {d['name']}/")
            lines.extend(self._format_tree(d, prefix + "  "))

        for f in files:
            icon = "⭐" if f.get("is_key") else "📄"
            lines.append(f"{prefix}{icon} {f['name']}")

        return "
".join(lines)
