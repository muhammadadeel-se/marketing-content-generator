import sys
import os

# Root folder ko Python path mein add kar rahe hain taake generate_copy module mil sakay
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from generate_copy import generate_marketing_copy

def test_sample_product_1():
    description = "An automated sprint planning tool for agile software teams."
    result = generate_marketing_copy(description)
    
    assert isinstance(result, dict)
    assert "headline" in result
    assert "tagline" in result
    assert "body" in result
    assert len(result["headline"]) > 0

def test_sample_product_2():
    description = "A real-time bug tracking dashboard with instant Slack notifications."
    result = generate_marketing_copy(description)
    
    assert isinstance(result, dict)
    assert "headline" in result
    assert "tagline" in result
    assert "body" in result
    assert len(result["tagline"]) > 0

def test_sample_product_3():
    description = "An AI code reviewer that analyzes pull requests for security vulnerabilities."
    result = generate_marketing_copy(description)
    
    assert isinstance(result, dict)
    assert "headline" in result
    assert "tagline" in result
    assert "body" in result
    assert len(result["body"]) > 0


def test_falls_back_without_openai(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = generate_marketing_copy("A workflow automation platform for product teams.")

    assert isinstance(result, dict)
    assert set(["headline", "tagline", "body"]).issubset(result)
    assert len(result["headline"]) > 0
    assert len(result["tagline"]) > 0
    assert len(result["body"]) > 0