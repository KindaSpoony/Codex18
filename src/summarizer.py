"""Summarizer module for generating OODA-style summaries via OpenAI."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        filename="summarizer.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )


class Summarizer:
    """Generate structured OODA summaries using the OpenAI API."""

    def __init__(self, *, model: str = "gpt-4-turbo", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_prompt(self, text: str) -> str:
        return (
            "Using the OODA loop format (Observe, Orient, Decide, Act), "
            "summarize the following intelligence:\n\n"
            f"{text}\n\n"
            "Output the summary strictly as structured JSON with keys: "
            "Observe, Orient, Decide, Act."
        )

    def _call_openai(self, prompt: str) -> str:
        """Call the OpenAI chat completion API and return the raw JSON text."""
        try:
            import openai
            from openai import OpenAIError
        except Exception as exc:  # pragma: no cover - dependency missing
            logger.error("OpenAI library not available: %s", exc, exc_info=True)
            raise RuntimeError("OpenAI library not available") from exc

        try:
            if hasattr(openai, "OpenAI"):
                client = openai.OpenAI(api_key=self.api_key)
                resp = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an intelligence analyst."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.2,
                )
                return resp.choices[0].message.content
            else:
                openai.api_key = self.api_key
                resp = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an intelligence analyst."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.2,
                )
                return resp["choices"][0]["message"]["content"]
        except OpenAIError as exc:  # type: ignore
            logger.error("OpenAI API error: %s", exc, exc_info=True)
            raise RuntimeError("Summarization failed") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def summarize(self, input_data: Dict[str, Any]) -> Dict[str, str]:
        """Return an OODA summary dictionary for ``input_data``."""
        if not isinstance(input_data, dict):
            raise TypeError("input_data must be a dictionary")

        logger.info("Input JSON: %s", json.dumps(input_data))

        text = input_data.get("text")
        if not text:
            text = json.dumps(input_data)

        prompt = self._build_prompt(text)
        summary_text = self._call_openai(prompt)
        try:
            summary = json.loads(summary_text)
        except Exception as exc:
            logger.error("Failed to parse summary JSON: %s", exc, exc_info=True)
            raise RuntimeError("Invalid summary format") from exc

        expected_keys = {"Observe", "Orient", "Decide", "Act"}
        if set(summary.keys()) != expected_keys:
            raise AssertionError("Summary must contain exactly Observe, Orient, Decide, Act")
        for key, value in summary.items():
            assert isinstance(value, str) and value.strip(), f"{key} should be a non-empty string"

        logger.info("Summary: %s", json.dumps(summary))
        return summary


__all__ = ["Summarizer"]
