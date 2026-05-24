"""Pydantic schemas for agent outputs."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class VegaOutput(BaseModel):
    regime_signal: Literal["RISK_ON", "CAUTIOUS", "RISK_OFF"]
    confidence_pct: float = Field(ge=0, le=100)
    key_risk_factors: list[str] = Field(default_factory=list, max_length=10)
    macro_thesis: str = Field(max_length=1200)
    halt_recommendation: bool


class SentinelOutput(BaseModel):
    attention_required: bool
    alert_level: Literal["INFO", "WATCH", "INVESTIGATE", "HIGH_ALERT", "TRADE_CANDIDATE", "BLOCKED"]
    priority_score: float = Field(ge=0, le=1)
    reason: str = Field(max_length=700)


class NysaOutput(BaseModel):
    sentiment_score: float = Field(ge=-1, le=1)
    catalyst_tags: list[str] = Field(default_factory=list, max_length=10)
    red_flag: bool
    red_flag_severity: float = Field(ge=0, le=1)
    news_summary: str = Field(max_length=700)
    retrieved_similar_events: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("catalyst_tags")
    @classmethod
    def tags_must_be_known(cls, tags: list[str]) -> list[str]:
        valid = {
            "EARNINGS_BEAT",
            "EARNINGS_MISS",
            "MGMT_CHANGE",
            "USFDA_ALERT",
            "ORDER_WIN",
            "BLOCK_DEAL",
            "PLEDGE",
            "AUDITOR_RESIGNATION",
            "GUIDANCE_CHANGE",
            "REGULATORY_ACTION",
        }
        return [tag for tag in tags if tag in valid]


class QuantraOutput(BaseModel):
    factor_attribution: dict[str, dict[str, str | float]]
    composite_score: float = Field(ge=0, le=1)
    timeframe_recommendation: Literal["monthly", "quarterly", "annual"]
    invalidation_conditions: list[str] = Field(default_factory=list, max_length=10)
    entry_logic_paragraph: str = Field(max_length=900)


class LexaOutput(BaseModel):
    moat_score: float = Field(ge=0, le=5)
    quality_assessment: str = Field(max_length=1200)
    risk_flags: list[str] = Field(default_factory=list, max_length=10)
    valuation_band: dict[str, float]
    fundamental_thesis: str = Field(max_length=1800)
    red_flag: bool


class SectoraOutput(BaseModel):
    sector_outlook: Literal["BULLISH", "NEUTRAL", "BEARISH"]
    leadership_stocks: list[str] = Field(default_factory=list, max_length=10)
    laggard_stocks: list[str] = Field(default_factory=list, max_length=10)
    rotation_thesis: str = Field(max_length=900)
    sector_risk_factors: list[str] = Field(default_factory=list, max_length=10)


class VeraOutput(BaseModel):
    veto: bool
    veto_reason: str | None = None
    risk_score: float = Field(ge=0, le=1)
    unchecked_risks: list[str] = Field(default_factory=list, max_length=10)
    confidence_adjustment: float = Field(ge=-0.3, le=0)
    verification_report: str = Field(max_length=1200)


class ApexOutput(BaseModel):
    decision: Literal["PROCEED", "SKIP"]
    entry_price: float | None = None
    stop_price: float | None = None
    target_price: float | None = None
    timeframe: str | None = None
    confidence: float = Field(ge=0, le=1)
    final_thesis: str = Field(max_length=1500)
    agent_agreement_score: float = Field(ge=0, le=1)
    dissenting_agent: str | None = None
    vector_id: str | None = None
