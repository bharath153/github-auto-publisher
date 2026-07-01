"""GitHub repository manager."""
import os
from pathlib import Path
from typing import Optional, List
from github import Github, GithubException
from git import Repo


class GitHubManager:
    """Manages GitHub repository operations."""

    def __init__(self, token: str):
        self.github = Github(token)
        self.user = self.github.get_user()

    def create_repository(
        self,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = False
    ) -> str:
        """Create a new GitHub repository. Returns the clone URL."""
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init
            )
            return repo.clone_url
        except GithubException as e:
            if e.status == 422:
                raise ValueError(f"Repository '{name}' already exists or name is invalid")
            raise

    def push_local_project(
        self,
        local_path: str,
        repo_url: str,
        commit_message: str = "Initial commit",
        generated_files: Optional[dict] = None
    ):
        """Push a local project to a GitHub repository."""
        local_path = Path(local_path)

        # Initialize git repo if not exists
        if not (local_path / ".git").exists():
            repo = Repo.init(local_path)
        else:
            repo = Repo(local_path)

        # Add remote
        if "origin" not in [r.name for r in repo.remotes]:
            repo.create_remote("origin", repo_url)
        else:
            repo.remotes.origin.set_url(repo_url)

        # Write generated files
        if generated_files:
            for filename, content in generated_files.items():
                file_path = local_path / filename
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

        # Add all files
        repo.git.add(A=True)

        # Commit
        if repo.is_dirty(untracked_files=True):
            repo.index.commit(commit_message)

        # Push to main branch
        origin = repo.remotes.origin
        origin.push(refspec="main:main", force=True)

        return repo

    def get_repo_info(self, repo_name: str) -> dict:
        """Get information about a repository."""
        repo = self.user.get_repo(repo_name)
        return {
            "name": repo.name,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language,
            "description": repo.description,
        }
