"""What the risk classifier submits: one AI Act tier with grounded reasons, and its tool schema."""

from __future__ import annotations

from typing import Any, Literal, get_args

from pydantic import BaseModel, Field

Tier = Literal["prohibited", "high_risk", "transparency_only", "minimal_risk", "needs_more_info"]
TIERS: tuple[str, ...] = get_args(Tier)
DISCLAIMER = "Information only, not legal advice."  # added by whoever shows the result
# The articles a tier must cite (article-level ids); the other tiers have no rule of their own.
TIER_ARTICLES = {
    "prohibited": ("AIA-Art5",),
    "high_risk": ("AIA-Art6", "AIA-AnnexI", "AIA-AnnexIII"),
    "transparency_only": ("AIA-Art50",),
}


class Classification(BaseModel):
    """The final AI Act classification of the described AI system."""

    tier: Tier
    reasons: list[str] = Field(min_length=1, description="Short reasons, one per rule checked")
    citations: list[str] = Field(
        min_length=1, description="Ids returned by search_ai_act, such as AIA-Art6-2"
    )
    confidence: float = Field(ge=0, le=1)
    follow_up_questions: list[str] = Field(
        default_factory=list, description="The facts to ask for when the tier is needs_more_info"
    )


def tool_schema(model: type[BaseModel]) -> dict[str, Any]:
    """The model's JSON schema without `title` keys, which some providers reject."""

    def strip(node: Any) -> Any:
        """The node without its `title` keys, at every depth."""
        if isinstance(node, dict):
            return {key: strip(value) for key, value in node.items() if key != "title"}
        if isinstance(node, list):
            return [strip(value) for value in node]
        return node

    return strip(model.model_json_schema())
