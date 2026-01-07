"""
Unit tests for task_status_updater module.

Tests checkbox replacement, task ID extraction, thread safety, and error handling.
"""

import tempfile
import threading
from pathlib import Path

import pytest

from specify_cli.task_status_updater import TaskStatusUpdater, TaskUpdate


class TestTaskStatusUpdater:
    """Test suite for TaskStatusUpdater class."""

    def test_update_task_success(self):
        """Test successful task update: [ ] → [x]"""
        # Create temporary tasks.md
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("# Tasks\n\n- [ ] T001 Create User model\n- [ ] T002 Test User model\n")
            f.flush()
            tasks_path = f.name

        try:
            # Initialize updater
            updater = TaskStatusUpdater(tasks_path)

            # Update T001 as successful
            task_update = TaskUpdate(
                task_id="T001",
                task_name="Create User model",
                success=True,
                duration_ms=1500,
            )

            success, error = updater.update_task_status(task_update)

            # Verify update successful
            assert success is True
            assert error is None

            # Verify file content
            with open(tasks_path, "r") as f:
                content = f.read()
                assert "- [x] T001 Create User model" in content
                assert "- [ ] T002 Test User model" in content  # Other task unchanged

        finally:
            Path(tasks_path).unlink()

    def test_update_task_failure(self):
        """Test failed task update: [ ] → [!] + error comment"""
        # Create temporary tasks.md
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("# Tasks\n\n- [ ] T001 [P] [US1] Create User model in src/models/user.py\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)

            # Update T001 as failed
            task_update = TaskUpdate(
                task_id="T001",
                task_name="Create User model",
                success=False,
                error_message="Module not found: src.models",
                duration_ms=500,
            )

            success, error = updater.update_task_status(task_update)

            assert success is True
            assert error is None

            # Verify file content
            with open(tasks_path, "r") as f:
                content = f.read()
                assert "- [!] T001 [P] [US1] Create User model" in content
                assert "⚠️ ERROR: Module not found: src.models" in content

        finally:
            Path(tasks_path).unlink()

    def test_preserve_markers(self):
        """Test that task markers [P], [US1], [DEP:], [FR:] are preserved"""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("- [ ] T005 [P] [US1] [DEP:T001,T002] [FR:FR-001] Implement service\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)

            task_update = TaskUpdate(
                task_id="T005",
                task_name="Implement service",
                success=True,
            )

            success, error = updater.update_task_status(task_update)

            assert success is True

            with open(tasks_path, "r") as f:
                content = f.read()
                # All markers should be preserved
                assert "[P]" in content
                assert "[US1]" in content
                assert "[DEP:T001,T002]" in content
                assert "[FR:FR-001]" in content
                assert "- [x] T005 [P] [US1]" in content

        finally:
            Path(tasks_path).unlink()

    def test_task_not_found(self):
        """Test updating non-existent task returns error"""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("- [ ] T001 Create model\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)

            task_update = TaskUpdate(
                task_id="T999",  # Does not exist
                task_name="Non-existent task",
                success=True,
            )

            success, error = updater.update_task_status(task_update)

            assert success is False
            assert "T999 not found" in error

        finally:
            Path(tasks_path).unlink()

    def test_concurrent_updates(self):
        """Test concurrent updates from multiple threads don't corrupt file"""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            # Create 5 tasks
            for i in range(1, 6):
                f.write(f"- [ ] T00{i} Task {i}\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)
            threads = []
            results = []

            def update_task(task_num):
                """Update a task in a separate thread."""
                task_update = TaskUpdate(
                    task_id=f"T00{task_num}",
                    task_name=f"Task {task_num}",
                    success=True,
                )
                result = updater.update_task_status(task_update)
                results.append(result)

            # Launch 5 threads updating different tasks
            for i in range(1, 6):
                t = threading.Thread(target=update_task, args=(i,))
                threads.append(t)
                t.start()

            # Wait for all threads
            for t in threads:
                t.join()

            # Verify all updates successful
            for success, error in results:
                assert success is True
                assert error is None

            # Verify file has all 5 tasks marked [x]
            with open(tasks_path, "r") as f:
                content = f.read()
                for i in range(1, 6):
                    assert f"- [x] T00{i} Task {i}" in content

        finally:
            Path(tasks_path).unlink()

    def test_extract_task_id_from_name(self):
        """Test task ID extraction from agent task names"""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("- [ ] T001 Create User model in src/models/user.py\n")
            f.write("- [ ] T002 Test User model\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)

            with open(tasks_path, "r") as f:
                content = f.read()

            # Test direct extraction (name has T### prefix)
            task_id = updater.find_task_id_from_name("T001-create-user-model", content)
            assert task_id == "T001"

            # Test lowercase
            task_id = updater.find_task_id_from_name("t002-test-model", content)
            assert task_id == "T002"

            # Test fallback to content search
            task_id = updater.find_task_id_from_name("Create User model", content)
            assert task_id == "T001"

            # Test not found
            task_id = updater.find_task_id_from_name("Nonexistent task", content)
            assert task_id is None

        finally:
            Path(tasks_path).unlink()

    def test_missing_file(self):
        """Test graceful error when tasks.md doesn't exist"""
        updater = TaskStatusUpdater("/nonexistent/path/tasks.md")

        task_update = TaskUpdate(
            task_id="T001",
            task_name="Task",
            success=True,
        )

        success, error = updater.update_task_status(task_update)

        assert success is False
        assert "not found" in error.lower()

    def test_multiple_tasks_with_similar_ids(self):
        """Test that T001 doesn't match T0011 (word boundary check)"""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("- [ ] T001 Task one\n")
            f.write("- [ ] T0011 Task eleven\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)

            # Update T001
            task_update = TaskUpdate(
                task_id="T001",
                task_name="Task one",
                success=True,
            )

            success, error = updater.update_task_status(task_update)
            assert success is True

            with open(tasks_path, "r") as f:
                content = f.read()
                # T001 should be updated
                assert "- [x] T001 Task one" in content
                # T0011 should NOT be touched
                assert "- [ ] T0011 Task eleven" in content

        finally:
            Path(tasks_path).unlink()

    def test_default_error_message(self):
        """Test that default 'Task failed' message is used when error_message is None"""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as f:
            f.write("- [ ] T001 Task\n")
            f.flush()
            tasks_path = f.name

        try:
            updater = TaskStatusUpdater(tasks_path)

            task_update = TaskUpdate(
                task_id="T001",
                task_name="Task",
                success=False,
                error_message=None,  # No specific error
            )

            success, error = updater.update_task_status(task_update)
            assert success is True

            with open(tasks_path, "r") as f:
                content = f.read()
                assert "⚠️ ERROR: Task failed" in content

        finally:
            Path(tasks_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
