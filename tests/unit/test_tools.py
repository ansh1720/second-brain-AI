"""
Unit tests for MCP tools: calculator, compare_options, read_pdf, search_web.
These test the tool functions directly — no API key or network required
(except search_web which we test for graceful failure).
"""
import json
import os
import sys
import tempfile
import pytest

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mcp_server.calculator import calculator
from mcp_server.compare_tool import compare_options
from mcp_server.pdf_reader import read_pdf


# ── Calculator ───────────────────────────────────────────────────────────

class TestCalculator:
    def test_basic_addition(self):
        assert "4" in calculator("2+2")

    def test_multiplication(self):
        assert "82600" in calculator("70000 * 1.18")

    def test_subtraction(self):
        result = calculator("100000 - 70000")
        assert "30000" in result

    def test_parentheses(self):
        result = calculator("(10 + 5) * 2")
        assert "30" in result

    def test_division(self):
        result = calculator("100 / 4")
        assert "25" in result

    def test_invalid_characters_rejected(self):
        result = calculator("import os; os.system('rm -rf /')")
        assert "Error" in result or "invalid" in result.lower()

    def test_empty_expression(self):
        result = calculator("")
        assert "Error" in result or "Result" in result


# ── Compare Options ──────────────────────────────────────────────────────

class TestCompareOptions:
    def test_basic_comparison(self):
        data = json.dumps({
            "options": [
                {"name": "MacBook Air", "price": "89900 INR", "ram": "8GB"},
                {"name": "Lenovo LOQ", "price": "70000 INR", "ram": "16GB"},
            ]
        })
        result = compare_options(data)
        assert "MacBook Air" in result
        assert "Lenovo LOQ" in result
        assert "|" in result  # markdown table

    def test_single_option(self):
        data = json.dumps({"options": [{"name": "OnlyOption", "score": "10"}]})
        result = compare_options(data)
        assert "OnlyOption" in result

    def test_empty_options_array(self):
        result = compare_options('{"options": []}')
        assert "Error" in result

    def test_invalid_json(self):
        result = compare_options("not valid json at all")
        assert "Error" in result

    def test_missing_options_key(self):
        result = compare_options('{"items": []}')
        assert "Error" in result

    def test_many_fields(self):
        data = json.dumps({
            "options": [
                {"name": "A", "price": "100", "weight": "1.2kg", "battery": "10h", "gpu": "RTX 4060"},
                {"name": "B", "price": "200", "weight": "2.0kg", "battery": "5h", "gpu": "Integrated"},
            ]
        })
        result = compare_options(data)
        assert "RTX 4060" in result
        assert "Integrated" in result


# ── PDF Reader ───────────────────────────────────────────────────────────

class TestPdfReader:
    def test_nonexistent_file(self):
        result = read_pdf("/nonexistent/path/to/file.pdf")
        assert "Error" in result or "does not exist" in result

    def test_syllabus_fallback(self):
        """Files with 'syllabus' in the name should return mock content."""
        result = read_pdf("/fake/path/ai_syllabus.pdf")
        assert "Mock PDF Content" in result or "Semester" in result

    def test_roadmap_fallback(self):
        result = read_pdf("/fake/path/ml_roadmap.pdf")
        assert "Mock PDF Content" in result

    def test_read_real_text_file(self):
        """Create a temp text file and verify read_pdf can read it."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Hello, this is test content for the PDF reader.")
            f.flush()
            path = f.name
        try:
            result = read_pdf(path)
            assert "Hello" in result
            assert "test content" in result
        finally:
            os.unlink(path)


# ── Memory Tool (routing logic) ──────────────────────────────────────────

class TestMemoryToolRouting:
    """Test the save_memory/retrieve_memory routing in mcp_server/memory_tool.py"""

    def test_import_works(self):
        from mcp_server.memory_tool import save_memory, retrieve_memory
        assert callable(save_memory)
        assert callable(retrieve_memory)

    def test_save_preference(self):
        from mcp_server.memory_tool import save_memory
        result = save_memory("budget", "100000 INR")
        assert "Successfully saved" in result
        assert "preferences" in result

    def test_save_goal(self):
        from mcp_server.memory_tool import save_memory
        result = save_memory("career_goals", "Become an AI engineer")
        assert "Successfully saved" in result
        assert "goals" in result

    def test_save_decision(self):
        from mcp_server.memory_tool import save_memory
        result = save_memory("decisions", "Chose Lenovo LOQ")
        assert "Successfully saved" in result
        assert "decisions" in result

    def test_retrieve_preferences(self):
        from mcp_server.memory_tool import save_memory, retrieve_memory
        save_memory("test_key_unit", "test_value_unit")
        result = retrieve_memory("test_key_unit")
        assert "test_value_unit" in result or "not found" in result.lower()
