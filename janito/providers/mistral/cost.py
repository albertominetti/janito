"""Cost estimation for the Mistral AI provider.

Rates source
------------
The per-1M-token rates below are the list prices from the official Mistral
pricing page at https://docs.mistral.ai/getting-started/pricing/
(last verified 2026-10-09) and apply as of the verification date.  Mistral
announced a 50% launch discount for 2 weeks after the Large 4 release, so
the page shows sale rates struck against these list rates; the list rates
are used here as the stable default.  Mistral adjusts figures frequently,
so cross-check that page before relying on them.

Prompt caching
--------------
Repeated input tokens (a stable system prompt, a long document, few-shot
examples) are billed at the much lower cache-hit rate instead of the
cache-miss rate.
"""

#: Per-1M-token rates (USD) keyed by model name:
#: ``(input cache miss, input cache hit, output)``.
_MODEL_RATES: dict[str, tuple[float, float, float]] = {
    "mistral-large-4": (1.36, 0.14, 4.18),
}


def get_cost(
    model: str,
    input: int,
    output: int,
    cached: int,
    is_reference: bool = False,
) -> str:
    """Estimate the monetary cost of a request in dollars.

    Args:
        model: The model name used for the request.
        input: The number of input tokens.
        output: The number of output tokens.
        cached: The number of cached input tokens (cache reads).
        is_reference: Marks the request as a reference request (e.g. tokens
            from attached reference documents).  Passed through for future
            reference-token billing; currently the estimate is unchanged.

    Returns:
        The estimated cost formatted as a dollar string with six decimal
        digits (e.g. ``"2.500000$"``), or ``"N/A"`` for an unknown model.
    """
    rates = _MODEL_RATES.get(model)
    if rates is None:
        return "N/A"
    input_miss, input_hit, output_rate = rates
    cost = ((input - cached) * input_miss + cached * input_hit + output * output_rate) / 1_000_000
    return f"{cost:.6f}$"
