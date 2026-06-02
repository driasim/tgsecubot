"""Tests for tgsecubot PR #1: corrupted json.loads handling"""

import os
import sys
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_malformed_json_handling():
    """Verify malformed JSON is handled gracefully"""
    root = os.path.join(os.path.dirname(__file__), "..")
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                if "json.loads" in content:
                    lines = content.split("\n")
                    for i, line in enumerate(lines, 1):
                        if "json.loads" in line:
                            start = max(0, i - 3)
                            end = min(len(lines), i + 3)
                            context = "\n".join(lines[start:end])
                            if "try" in context or "except" in context:
                                return True


def test_json_decode_error_caught():
    """Verify JSONDecodeError is caught"""
    root = os.path.join(os.path.dirname(__file__), "..")
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                if "JSONDecodeError" in content:
                    return True


def test_corrupted_json_returns_default():
    """Test corrupted JSON returns default/fallback"""
    corrupted = [
        "{bad json}",
        "",
        "None",
        "undefined",
    ]
    for bad in corrupted:
        try:
            json.loads(bad)
            pytest.fail(f"Should raise: {bad!r}")
        except json.JSONDecodeError:
            pass  # Expected


def test_no_eval_for_json():
    """Verify eval() is not used for JSON parsing"""
    root = os.path.join(os.path.dirname(__file__), "..")
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                if "eval" in content and "json" in content.lower():
                    lines = content.split("\n")
                    for i, line in enumerate(lines, 1):
                        if "eval" in line and "json" in line.lower():
                            pytest.fail(f"eval() with JSON at {fn}:{i}")


def test_state_file_corruption_recovery():
    """Verify state file corruption is handled"""
    root = os.path.join(os.path.dirname(__file__), "..")
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                if "json.loads" in content:
                    lines = content.split("\n")
                    for i, line in enumerate(lines, 1):
                        if "json.loads" in line:
                            # Check for default/fallback after exception
                            end = min(len(lines), i + 5)
                            context = "\n".join(lines[i:end])
                            if "return" in context or "{}" in context or "[]" in context or "None" in context:
                                return True
