"""Accepted --model values, provider routes, API ids, and list pricing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping

Transport = Literal["anthropic", "requesty"]


@dataclass(frozen=True)
class ModelSpec:
    """One accepted --model flag value."""

    flag: str  # CLI string, e.g. gemini-2.5-flash
    slug: str  # filesystem / trial_id component
    api_model: str  # verbatim provider model id recorded in run metadata
    input_usd_per_mtok: float
    output_usd_per_mtok: float
    display: str
    transport: Transport
    provider: str  # anthropic | google | openai
    provider_route: str  # Requesty prefix (google/…) or anthropic-direct
    runnable: bool = True
    notes: str = ""


# Active + registered-fallback models. Sonnet / gpt-5-mini intentionally absent.
MODEL_PRICING: dict[str, ModelSpec] = {
    "claude-haiku-4.5": ModelSpec(
        flag="claude-haiku-4.5",
        slug="claude-haiku-4.5",
        api_model="claude-haiku-4-5-20251001",
        input_usd_per_mtok=1.0,
        output_usd_per_mtok=5.0,
        display="Claude Haiku 4.5",
        transport="anthropic",
        provider="anthropic",
        provider_route="anthropic-direct",
        runnable=True,
        notes="Phase 1 full grid (Anthropic Messages API).",
    ),
    "gemini-2.5-flash": ModelSpec(
        flag="gemini-2.5-flash",
        slug="gemini-2.5-flash",
        # Pin GOOGLE provider route explicitly — never the Coding route
        # that shares the same short name in the Requesty library.
        api_model="google/gemini-2.5-flash",
        input_usd_per_mtok=0.30,
        output_usd_per_mtok=2.50,
        display="Gemini 2.5 Flash (Google via Requesty)",
        transport="requesty",
        provider="google",
        provider_route="google",
        runnable=True,
        notes=(
            "Phase 2 probe partially complete; FULL GRID SUSPENDED "
            "(Google route quota ~5–6 trials/sitting). 6 valid cells banked; "
            "36 pending remain resumable via --retry-failed. "
            "api_model pinned to google/."
        ),
    ),
    "gpt-5-nano": ModelSpec(
        flag="gpt-5-nano",
        slug="gpt-5-nano",
        api_model="openai/gpt-5-nano",
        input_usd_per_mtok=0.05,
        output_usd_per_mtok=0.40,
        display="GPT-5 nano (OpenAI via Requesty)",
        transport="requesty",
        provider="openai",
        provider_route="openai",
        runnable=True,
        notes=(
            "Phase 2b/3 active path after gemini full-grid suspension. "
            "ID+pricing confirmed from Requesty library: openai/gpt-5-nano "
            "at $0.05/M in, $0.40/M out (OpenAI route)."
        ),
    ),
}

DEFAULT_MODEL = "claude-haiku-4.5"
ACCEPTED_MODELS: tuple[str, ...] = tuple(MODEL_PRICING.keys())
RUNNABLE_MODELS: tuple[str, ...] = tuple(
    k for k, v in MODEL_PRICING.items() if v.runnable
)

# Explicitly excluded from the printed plan / registry (do not resurrect quietly).
EXCLUDED_FROM_PLAN: tuple[str, ...] = (
    "claude-sonnet-4-5",
    "gpt-5-mini",
)


class UnknownModelError(ValueError):
    """Raised when --model is not in MODEL_PRICING."""


class BlockedModelError(ValueError):
    """Raised when a registered model is not runnable yet."""


def resolve_model(model: str, *, require_runnable: bool = True) -> ModelSpec:
    """Resolve a --model flag (or known alias) to a ModelSpec; fail loudly if unknown."""
    key = (model or "").strip()
    if key in MODEL_PRICING:
        spec = MODEL_PRICING[key]
    else:
        spec = None
        for candidate in MODEL_PRICING.values():
            if key in (candidate.slug, candidate.api_model):
                spec = candidate
                break
        if spec is None:
            raise UnknownModelError(
                f"Unknown model {model!r}. Accepted --model values: "
                f"{', '.join(ACCEPTED_MODELS)}. "
                f"Excluded from plan (not registered): {', '.join(EXCLUDED_FROM_PLAN)}. "
                f"Add pricing + provider route to MODEL_PRICING before using a new model."
            )
    if require_runnable and not spec.runnable:
        raise BlockedModelError(
            f"Model {spec.flag!r} is registered but placeholder-blocked "
            f"({spec.notes or 'no notes'})."
        )
    return spec


def model_slug(model: str) -> str:
    return resolve_model(model, require_runnable=False).slug


def assert_pricing_covers_accepted() -> None:
    """Hermetic: every ACCEPTED_MODELS entry has a MODEL_PRICING row."""
    missing = [m for m in ACCEPTED_MODELS if m not in MODEL_PRICING]
    if missing:
        raise AssertionError(f"MODEL_PRICING missing entries for {missing}")
    for flag, spec in MODEL_PRICING.items():
        if flag != spec.flag:
            raise AssertionError(f"MODEL_PRICING key {flag!r} != spec.flag {spec.flag!r}")
        if spec.input_usd_per_mtok <= 0 or spec.output_usd_per_mtok <= 0:
            raise AssertionError(f"{flag}: pricing must be positive")
        if not spec.slug or not spec.api_model:
            raise AssertionError(f"{flag}: slug and api_model required")
        if spec.transport == "requesty":
            # Provider route must be an explicit prefix on the api_model.
            prefix = f"{spec.provider_route}/"
            if not spec.api_model.startswith(prefix):
                raise AssertionError(
                    f"{flag}: requesty api_model {spec.api_model!r} must start "
                    f"with pinned provider route {prefix!r}"
                )
        if flag in EXCLUDED_FROM_PLAN:
            raise AssertionError(f"{flag} must stay out of MODEL_PRICING")
    for excluded in EXCLUDED_FROM_PLAN:
        if excluded in MODEL_PRICING:
            raise AssertionError(f"{excluded} must remain excluded from registry")


def blended_usd_per_mtok(spec: ModelSpec, *, input_share: float = 0.8) -> float:
    """Blended $/MTok assuming input_share of tokens are input."""
    out_share = 1.0 - input_share
    return (
        input_share * spec.input_usd_per_mtok
        + out_share * spec.output_usd_per_mtok
    )


def pricing_table_rows() -> Mapping[str, ModelSpec]:
    return MODEL_PRICING


def metadata_for_spec(spec: ModelSpec) -> dict[str, str | float | bool]:
    """Fields recorded verbatim on every trial / gate printout."""
    return {
        "model": spec.flag,
        "model_slug": spec.slug,
        "api_model": spec.api_model,
        "provider": spec.provider,
        "provider_route": spec.provider_route,
        "transport": spec.transport,
        "input_usd_per_mtok": spec.input_usd_per_mtok,
        "output_usd_per_mtok": spec.output_usd_per_mtok,
    }
