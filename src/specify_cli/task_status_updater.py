"""
Task status updater for tasks.md file manipulation.

Handles automatic checkbox updates during /speckit.implement execution.
Thread-safe for concurrent wave execution.
"""

import re
import platform
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

# Platform-specific file locking
if platform.system() == "Windows":
    import msvcrt

    def lock_file(f):
        """Acquire exclusive lock on Windows."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

    def unlock_file(f):
        """Release lock on Windows."""
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def lock_file(f):
        """Acquire exclusive lock on Unix."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    def unlock_file(f):
        """Release lock on Unix."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


@dataclass
class TaskUpdate:
    """Represents a task status update."""

    task_id: str  # e.g., "T001"
    task_name: str  # Agent task name
    success: bool
    error_message: Optional[str] = None
    duration_ms: int = 0


class TaskStatusUpdater:
    """
    Thread-safe updater for tasks.md checkbox status.

    Uses file locking to prevent corruption during concurrent updates.
    """

    def __init__(self, tasks_file_path: str):
        """
        Initialize updater with path to tasks.md.

        Args:
            tasks_file_path: Absolute path to tasks.md file
        """
        self.tasks_file_path = Path(tasks_file_path)
        self._lock = threading.Lock()  # Python-level lock

    def update_task_status(
        self, task_update: TaskUpdate
    ) -> Tuple[bool, Optional[str]]:
        """
        Update task status in tasks.md file.

        Args:
            task_update: TaskUpdate object with status info

        Returns:
            Tuple of (success: bool, error_message: Optional[str])

        Thread-safe: Uses both threading.Lock and file locking
        """
        with self._lock:  # Python-level lock for thread safety
            try:
                # Validate file exists
                if not self.tasks_file_path.exists():
                    return (
                        False,
                        f"tasks.md not found at {self.tasks_file_path}",
                    )

                # Read file with OS-level lock
                with open(
                    self.tasks_file_path, "r+", encoding="utf-8"
                ) as f:
                    # Acquire exclusive lock (blocks if another process has lock)
                    lock_file(f)

                    try:
                        content = f.read()

                        # Update content
                        updated_content, found = self._replace_checkbox(
                            content, task_update
                        )

                        if not found:
                            return (
                                False,
                                f"Task {task_update.task_id} not found in tasks.md",
                            )

                        # Write back atomically
                        f.seek(0)
                        f.write(updated_content)
                        f.truncate()

                        return (True, None)

                    finally:
                        # Release lock
                        unlock_file(f)

            except Exception as e:
                return (False, f"Failed to update tasks.md: {str(e)}")

    def _replace_checkbox(
        self, content: str, task_update: TaskUpdate
    ) -> Tuple[str, bool]:
        """
        Replace checkbox marker for a specific task.

        Args:
            content: Full tasks.md content
            task_update: Task update information

        Returns:
            Tuple of (updated_content, found)
        """
        # Pattern matches: - [ ] T001 (with any markers/description after)
        # Uses word boundary \b to avoid matching T0011 when looking for T001
        pattern = rf"^(\s*-\s*)\[\s*\]\s*({re.escape(task_update.task_id)}\b.*)$"

        found = False
        lines = content.split("\n")

        for i, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                indent = match.group(1)
                rest = match.group(2)

                if task_update.success:
                    # Success: - [x] T001 Description
                    lines[i] = f"{indent}[x] {rest}"
                else:
                    # Failure: - [!] T001 Description
                    # Add error message as indented comment on next line
                    error_msg = task_update.error_message or "Task failed"
                    error_comment = f"{indent}  ⚠️ ERROR: {error_msg}"
                    lines[i] = f"{indent}[!] {rest}"
                    # Insert error comment after current line
                    lines.insert(i + 1, error_comment)

                found = True
                break

        return ("\n".join(lines), found)

    def find_task_id_from_name(
        self, task_name: str, content: str
    ) -> Optional[str]:
        """
        Extract task ID from agent task name.

        Agent task names might be like "T001-create-user-model" or just task description.
        This tries to extract the T### ID.

        Args:
            task_name: Name from AgentTask.name
            content: tasks.md content to search

        Returns:
            Task ID (e.g., "T001") or None if not found
        """
        # Try direct extraction from name (e.g., "T001-description")
        task_id_match = re.match(r"^(T\d{3,})", task_name, re.IGNORECASE)
        if task_id_match:
            return task_id_match.group(1).upper()

        # Fallback: search for task name in content
        # This is less reliable but handles cases where task name doesn't include ID
        task_name_lower = task_name.lower()
        for line in content.split("\n"):
            if task_name_lower in line.lower():
                # Extract T### from line
                tid_match = re.search(r"\b(T\d{3,})\b", line)
                if tid_match:
                    return tid_match.group(1)

        return None
