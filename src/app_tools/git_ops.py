"""
Use GitPython to implement checkout_new_branch(name) and commit_changes(message). Use PyGithub to implement create_pull_request(...)."
"""
from app_utils.app_utils import GeneralUtils
from pathlib import Path
from git import Repo
from git.exc import GitCommandError
from github import Github
from github.GithubException import GithubException
import os
from dotenv import load_dotenv
from datetime import datetime
import textwrap
import black
from datetime import datetime

utils = GeneralUtils()
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def checkout_new_local_branch(in_local_repo_path: str, branch_name: str, pr_url: str) -> str:
    
    from pathlib import Path

    # Get the directory where main.py is located
    BASE_DIR_for_math_project = Path(__file__).parent.parent
    LOCAL_REPO_PATH = BASE_DIR_for_math_project / "self_project_data" 
    LOCAL_REPO_PATH.mkdir(parents=True, exist_ok=True)
    utils.print_n_from_left(source="GIT_OPS", msg=f"Generated project files will be stored in: {LOCAL_REPO_PATH}", n = 20)

    
    in_local_repo_path = Path(in_local_repo_path)
    downloaded_repo =prepare_monorepo(repo_url=pr_url, local_path=in_local_repo_path)

    # checkout a new branch
    git = downloaded_repo.git

    git.checkout('-b', branch_name)

    utils.print_n_from_left(source="GIT_OPS", msg=f"Checked out new branch: {branch_name}", n = 20)
    return branch_name

def create_local_temp_file(file_path: str, content: str):

    BASE_DIR_for_math_project = Path(__file__).parent.parent

    LOCAL_REPO_PATH = BASE_DIR_for_math_project / "self_project_data" 

    LOCAL_REPO_PATH_PROJECT = LOCAL_REPO_PATH / "math_project"

    file_name = f"math_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"

    full_file_path = file_path
    
    utils.print_n_from_left(source="GIT_OPS", msg=f"New file name: {full_file_path}", n = 20)

    clean_code = textwrap.dedent(content).strip()

    try:
        # Formats the string according to PEP 8 standards
        black_code = black.format_str(clean_code, mode=black.Mode())
    except black.InvalidInput:
        # If the AI generated invalid syntax, Black will fail
        utils.print_n_from_left(source="GIT_OPS", msg=f"black.format_str failed on content: {full_file_path}", n = 20)

    with open(full_file_path, "w") as f:
        f.write(black_code)

    return full_file_path


def commit_changes_and_push(commit_message: str):
    BASE_DIR_for_math_project = Path(__file__).parent.parent
    LOCAL_REPO_PATH = BASE_DIR_for_math_project / "self_project_data"
    LOCAL_REPO_PATH_PROJECT = LOCAL_REPO_PATH / "math_project"

    repo = Repo(LOCAL_REPO_PATH_PROJECT)

    repo.git.add(A=True)
    repo.index.commit(commit_message)

    try:
        branch = repo.active_branch.name
    except Exception:
        branch = repo.git.rev_parse('--abbrev-ref', 'HEAD').strip()

    try:
        repo.git.push('--set-upstream', 'origin', branch)
    except Exception:
        origin = repo.remote(name='origin')
        origin.push(refspec=f'{branch}:{branch}')

    utils.print_n_from_left(source="GIT_OPS", msg=f"Committed and pushed on branch: {branch} (message: {commit_message})", n = 20)


"""app_tools.git_ops
Small helper wrappers around GitPython and PyGithub used by the project.

This module centralizes repository path handling and provides utilities to:
- prepare or update a local clone of a repository
- create a local temp file (with optional black formatting)
- commit and push changes
- create a pull request via PyGithub

Keep function APIs stable to avoid breaking callers.
"""

from pathlib import Path
from datetime import datetime
import os
import textwrap
from typing import Optional

from git import Repo
from git.exc import GitCommandError
from github import Github
from github.GithubException import GithubException
from dotenv import load_dotenv
import black

from app_utils.app_utils import GeneralUtils

utils = GeneralUtils()
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Base directory for generated local state (used by functions below)
BASE_DIR = Path(__file__).parent.parent
LOCAL_REPO_DATA_DIR = BASE_DIR / "self_project_data"
LOCAL_REPO_DATA_DIR.mkdir(parents=True, exist_ok=True)


def checkout_new_local_branch(in_local_repo_path: str, branch_name: str, pr_url: str) -> str:
    """Prepare a local clone (or update it) and checkout a new branch.

    Returns the new branch name.
    """
    utils.print_n_from_left(source="GIT_OPS", msg=f"Generated project files will be stored in: {LOCAL_REPO_DATA_DIR}", n=20)

    in_local_repo_path = Path(in_local_repo_path)
    downloaded_repo = prepare_monorepo(repo_url=pr_url, local_path=in_local_repo_path)

    # checkout a new branch
    git = downloaded_repo.git
    git.checkout("-b", branch_name)

    utils.print_n_from_left(source="GIT_OPS", msg=f"Checked out new branch: {branch_name}", n=20)
    return branch_name


def create_local_temp_file(file_path: str, content: str) -> str:
    """Create a temporary Python file containing `content`.

    If `file_path` points to a directory, a filename is autogenerated.
    Attempts to format the code with Black; if Black fails, writes dedented content.
    Returns the path to the created file as a string.
    """
    LOCAL_REPO_PATH_PROJECT = LOCAL_REPO_DATA_DIR / "math_project"
    LOCAL_REPO_PATH_PROJECT.mkdir(parents=True, exist_ok=True)

    requested = Path(file_path)
    if requested.is_dir() or str(file_path).endswith(os.sep):
        file_name = f"math_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        full_file_path = requested / file_name
    else:
        full_file_path = requested

    utils.print_n_from_left(source="GIT_OPS", msg=f"New file name: {full_file_path}", n=20)

    clean_code = textwrap.dedent(content).strip() + "\n"

    try:
        # Formats the string according to PEP 8 standards
        black_code = black.format_str(clean_code, mode=black.Mode())
    except black.InvalidInput:
        # If Black fails (invalid syntax), fall back to the cleaned content
        utils.print_n_from_left(source="GIT_OPS", msg=f"black.format_str failed on content: {full_file_path}; writing unformatted content", n=20)
        black_code = clean_code

    # Ensure parent directory exists and write
    full_file_path = Path(full_file_path)
    full_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_file_path, "w", encoding="utf-8") as f:
        f.write(black_code)

    return str(full_file_path)


def commit_changes_and_push(commit_message: str) -> None:
    """Stage all changes, commit with `commit_message`, and push the current branch.

    Keeps existing fallback push behavior if direct push fails.
    """
    LOCAL_REPO_PATH_PROJECT = LOCAL_REPO_DATA_DIR / "math_project"
    repo = Repo(LOCAL_REPO_PATH_PROJECT)

    repo.git.add(A=True)
    repo.index.commit(commit_message)

    try:
        branch = repo.active_branch.name
    except Exception:
        branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()

    try:
        repo.git.push("--set-upstream", "origin", branch)
    except Exception:
        origin = repo.remote(name="origin")
        origin.push(refspec=f"{branch}:{branch}")

    utils.print_n_from_left(source="GIT_OPS", msg=f"Committed and pushed on branch: {branch} (message: {commit_message})", n=20)


def prepare_monorepo(repo_url: str, local_path: Path) -> Repo:
    """Clone the repo to `local_path` if missing, otherwise attempt to update it.

    Returns a GitPython `Repo` instance.
    """
    local_path = Path(local_path)

    if not (local_path / ".git").exists():
        utils.print_n_from_left(source="GIT_OPS", msg=f"Cloning monorepo from {repo_url}...", n=20)
        repo = Repo.clone_from(repo_url, local_path)
    else:
        repo = Repo(local_path)
        try:
            repo.remotes.origin.pull()
        except GitCommandError:
            # Fallback: fetch and attempt an explicit pull for the current branch
            try:
                repo.remotes.origin.fetch()
                try:
                    current_branch = repo.active_branch.name
                except Exception:
                    # Detached HEAD or no local branch; try to find main/master on origin
                    origin_refs = [r.name for r in repo.remotes.origin.refs]
                    if "origin/main" in origin_refs:
                        current_branch = "main"
                    elif "origin/master" in origin_refs:
                        current_branch = "master"
                    else:
                        current_branch = None

                if current_branch:
                    repo.git.checkout(current_branch)
                    repo.remotes.origin.pull("origin", current_branch)
            except Exception:
                # Best-effort only; leave the repo as-is on failure
                pass
    return repo


def create_pull_request(branch_name: str, title: str, body: str, repo_full_name: Optional[str] = "horasan/ai_self_math") -> str:
    """Create a pull request against `repo_full_name` from `branch_name` into `main`.

    If needed, attempts to use the authenticated user's fork notation for head.
    Returns the URL of the created pull request.
    """
    g = Github(GITHUB_TOKEN)

    repo = g.get_repo(repo_full_name)

    try:
        # If the branch exists on the upstream repo, use it directly
        repo.get_branch(branch_name)
        head = branch_name
    except GithubException:
        # Otherwise assume a fork with the current user's login
        try:
            user_login = g.get_user().login
            head = f"{user_login}:{branch_name}"
        except Exception:
            head = branch_name

    try:
        pull_request = repo.create_pull(title=title, body=body, head=head, base="main")
        utils.print_n_from_left(source="GIT_OPS", msg=f"Created pull request: {pull_request.html_url}", n=20)
        return pull_request.html_url
    except GithubException as e:
        utils.print_n_from_left(source="GIT_OPS", msg=f"Failed to create PR (head={head}): {getattr(e, 'data', str(e))}", n=20)
        raise
