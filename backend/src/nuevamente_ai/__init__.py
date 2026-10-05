"""Preparación y validación de prompts; sin clientes de IA ni llamadas de red."""

from .prompts import (
    AdaptationRequest, EvidenceChunk, PromptBundle, PromptRequest,
    build_from_contract, build_prompt, evidence_from_record,
)

__all__ = ["AdaptationRequest", "EvidenceChunk", "PromptBundle", "PromptRequest",
           "build_from_contract", "build_prompt", "evidence_from_record"]
