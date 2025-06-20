"""
Unit tests for UV/UVX configuration system
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Import the functions we want to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import apply_config, load_config_file


class TestUVConfig(unittest.TestCase):
    """Test UV/UVX configuration loading and application."""

    def setUp(self):
        """Set up test environment."""
        # Store original environment
        self.original_env = os.environ.copy()

    def tearDown(self):
        """Clean up test environment."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_load_config_file_valid_json(self):
        """Test loading a valid JSON configuration file."""
        config_data = {
            "api_keys": {
                "gemini": "test-gemini-key",
                "openai": "test-openai-key"
            },
            "settings": {
                "default_model": "pro",
                "log_level": "DEBUG"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            result = load_config_file(config_path)
            self.assertEqual(result, config_data)
        finally:
            os.unlink(config_path)

    def test_load_config_file_invalid_json(self):
        """Test loading an invalid JSON configuration file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{ invalid json }')
            config_path = f.name
        
        try:
            result = load_config_file(config_path)
            self.assertEqual(result, {})
        finally:
            os.unlink(config_path)

    def test_load_config_file_nonexistent(self):
        """Test loading a non-existent configuration file."""
        result = load_config_file('/nonexistent/path/config.json')
        self.assertEqual(result, {})

    def test_apply_config_api_keys(self):
        """Test applying API keys from configuration."""
        config = {
            "api_keys": {
                "gemini": "test-gemini-key",
                "openai": "test-openai-key",
                "xai": "test-xai-key"
            }
        }
        
        # Ensure environment variables are not set
        for key in ["GEMINI_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY"]:
            if key in os.environ:
                del os.environ[key]
        
        apply_config(config)
        
        self.assertEqual(os.environ.get("GEMINI_API_KEY"), "test-gemini-key")
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "test-openai-key")
        self.assertEqual(os.environ.get("XAI_API_KEY"), "test-xai-key")

    def test_apply_config_settings(self):
        """Test applying settings from configuration."""
        config = {
            "settings": {
                "default_model": "pro",
                "log_level": "DEBUG",
                "default_thinking_mode_thinkdeep": "medium"
            }
        }
        
        # Ensure environment variables are not set
        for key in ["DEFAULT_MODEL", "LOG_LEVEL", "DEFAULT_THINKING_MODE_THINKDEEP"]:
            if key in os.environ:
                del os.environ[key]
        
        apply_config(config)
        
        self.assertEqual(os.environ.get("DEFAULT_MODEL"), "pro")
        self.assertEqual(os.environ.get("LOG_LEVEL"), "DEBUG")
        self.assertEqual(os.environ.get("DEFAULT_THINKING_MODE_THINKDEEP"), "medium")

    def test_apply_config_does_not_override_existing_env(self):
        """Test that configuration does not override existing environment variables."""
        # Set existing environment variable
        os.environ["GEMINI_API_KEY"] = "existing-key"
        
        config = {
            "api_keys": {
                "gemini": "config-key"
            }
        }
        
        apply_config(config)
        
        # Should keep existing value
        self.assertEqual(os.environ.get("GEMINI_API_KEY"), "existing-key")

    def test_apply_config_empty_config(self):
        """Test applying empty configuration."""
        apply_config({})
        # Should not raise any errors

    def test_apply_config_none_values(self):
        """Test applying configuration with None values."""
        config = {
            "api_keys": {
                "gemini": None,
                "openai": "valid-key"
            }
        }
        
        apply_config(config)
        
        # None values should be ignored
        self.assertNotIn("GEMINI_API_KEY", os.environ)
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "valid-key")

    def test_full_config_integration(self):
        """Test full configuration integration with typical config file."""
        config_data = {
            "api_keys": {
                "gemini": "sk-gemini-test-key",
                "openai": "sk-openai-test-key",
                "xai": "xai-test-key",
                "openrouter": "sk-or-test-key"
            },
            "settings": {
                "default_model": "auto",
                "default_thinking_mode_thinkdeep": "high",
                "log_level": "INFO"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            # Clear relevant environment variables
            env_vars = [
                "GEMINI_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY", "OPENROUTER_API_KEY",
                "DEFAULT_MODEL", "DEFAULT_THINKING_MODE_THINKDEEP", "LOG_LEVEL"
            ]
            for var in env_vars:
                if var in os.environ:
                    del os.environ[var]
            
            # Load and apply configuration
            config = load_config_file(config_path)
            apply_config(config)
            
            # Verify all values are set correctly
            self.assertEqual(os.environ.get("GEMINI_API_KEY"), "sk-gemini-test-key")
            self.assertEqual(os.environ.get("OPENAI_API_KEY"), "sk-openai-test-key")
            self.assertEqual(os.environ.get("XAI_API_KEY"), "xai-test-key")
            self.assertEqual(os.environ.get("OPENROUTER_API_KEY"), "sk-or-test-key")
            self.assertEqual(os.environ.get("DEFAULT_MODEL"), "auto")
            self.assertEqual(os.environ.get("DEFAULT_THINKING_MODE_THINKDEEP"), "high")
            self.assertEqual(os.environ.get("LOG_LEVEL"), "INFO")
            
        finally:
            os.unlink(config_path)


if __name__ == "__main__":
    unittest.main()