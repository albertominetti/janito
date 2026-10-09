"""Tests for the Mistral AI provider (issue #27)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from conftest import make_config, make_ui_config

import janito.config_dir as config_dir_mod
from janito.auth_config import set_api_key


@pytest.fixture(autouse=True)
def _isolate_config_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(config_dir_mod, "_config_dir", tmp_path)
    set_api_key("mistral", "sk-test-mistral")


def _fake_run_returns(content, tool_calls=None):
    def fake_run(func, client, call_kwargs, tools_schemas):
        fake_run.captured_kwargs = call_kwargs
        fake_run.captured_tools = tools_schemas
        return content, None, tool_calls or {}, None, {}

    fake_run.captured_kwargs = None
    fake_run.captured_tools = None
    return fake_run


if pytest is not None:

    def test_mistral_provider_registered():
        from janito.providers.registry import get_provider
        from janito.providers.validation import list_supported_providers

        assert "mistral" in list_supported_providers()
        provider = get_provider("mistral")
        assert provider is not None
        assert provider.default_model() == "mistral-large-4"
        assert provider.model_names() == ["mistral-large-4"]
        # Case-insensitive lookup.
        assert get_provider("Mistral").default_model() == "mistral-large-4"

    def test_mistral_provider_config():
        from janito.providers.registry import get_provider

        provider = get_provider("mistral")
        assert provider.endpoint_for("Completions") == "https://api.mistral.ai/v1"
        assert provider.endpoint_for() == "https://api.mistral.ai/v1"
        entry = provider.model_config("mistral-large-4")
        assert entry.get("supported_api_types") == ["Completions"]
        assert entry.get("default_api_type") == "Completions"
        assert entry.get("max_input_tokens") == 1048576
        assert entry.get("max_output_tokens") == 262144
        assert entry.get("default_reasoning_effort") == "high"
        assert [e["effort"] for e in entry.get("supported_reasoning_efforts")] == [
            "low",
            "high",
            "max",
        ]

    def test_mistral_cost():
        from janito.providers.costing import get_provider_cost
        from janito.providers.mistral.cost import get_cost

        # List rates (1.36 / 0.14 / 4.18) per 1M tokens.
        assert get_cost("mistral-large-4", 1_000_000, 0, 0) == "1.360000$"
        assert get_cost("mistral-large-4", 1_000_000, 0, 500_000) == "0.750000$"
        assert get_cost("bogus-model", 10, 10, 0) == "N/A"
        assert get_provider_cost("mistral", "mistral-large-4", 1000, 1000, 0) != "N/A"
        assert get_provider_cost("Mistral", "mistral-large-4", 1000, 1000, 0) != "N/A"

    def test_mistral_run_turn_chat_and_reasoning():
        import janito.llm_clients.openai.completions_api as client_mod

        fake_run = _fake_run_returns("hello")
        config = make_config(
            provider="mistral",
            api_type="Completions",
            model="mistral-large-4",
            reasoning_effort="high",
            use_mcp=False,
        )
        result = client_mod.run_turn(config, "hi", ui_config=make_ui_config(stream_runner=fake_run))
        assert result == "hello"
        assert fake_run.captured_kwargs["reasoning_effort"] == "high"
        assert fake_run.captured_tools is not None

    def test_mistral_run_turn_advertises_function_tools():
        import janito.llm_clients.openai.completions_api as client_mod

        fake_run = _fake_run_returns("done")
        config = make_config(
            provider="mistral",
            api_type="Completions",
            model="mistral-large-4",
            use_mcp=False,
        )
        result = client_mod.run_turn(config, "hello", ui_config=make_ui_config(stream_runner=fake_run))
        assert result == "done"
        # Function tools are advertised to the model (tool-calling supported).
        assert fake_run.captured_tools
