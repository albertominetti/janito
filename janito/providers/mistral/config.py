"""Built-in configuration for the Mistral AI provider.

``PROVIDER_CONFIG`` is the config entry for ``mistral``.  See
:mod:`janito.providers.template.config` for the full reference of every
CONFIG option.
"""

#: The config entry for the ``mistral`` provider.
PROVIDER_CONFIG: dict = {
    "default_model": "mistral-large-4",
    "endpoint": "https://api.mistral.ai/v1",
    "models": {
        "mistral-large-4": {
            "supported_api_types": ["Completions"],
            "default_api_type": "Completions",  # built-in default (Completions-only)
            "max_input_tokens": 1048576,  # 1M
            "max_output_tokens": 262144,  # 256k
            # Per the Mistral reasoning docs, reasoning is adjustable via
            # the OpenAI-compatible reasoning_effort parameter. The docs
            # name none/low/high/max across models and report none and
            # high working for mistral-large-4-0; high is recommended for
            # agentic and code use cases, so it is the built-in default.
            # "none" is omitted: it collides with the /effort clear
            # keyword (see janito/shell/cmds/effort.py CLEAR_KEYWORDS).
            "default_reasoning_effort": "high",
            "supported_reasoning_efforts": [
                {
                    "effort": "low",
                    "description": "Lighter reasoning for fast responses",
                },
                {
                    "effort": "high",
                    "description": "Standard reasoning depth (the API default)",
                },
                {
                    "effort": "max",
                    "description": "Maximum reasoning depth for complex problems",
                },
            ],
        },
    },
}
