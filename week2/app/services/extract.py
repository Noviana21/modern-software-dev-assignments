from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(note_text: str) -> list[str]:
    system_prompt = (
        "You extract action items from notes. "
        "Return ONLY a JSON array of strings. "
        "No markdown, no code fences, no explanation."
    )
    user_prompt = (
        "Extract action items from the text below.\n\n"
        "Rules:\n"
        "1) Output must be a valid JSON array.\n"
        "2) Every element must be a string.\n"
        "3) If there are no action items, return [].\n\n"
        f"Text:\n{note_text}"
    )

    response = chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        format="json",
    )

    content = response.get("message", {}).get("content", "").strip()
    print(f"[DEBUG] Raw LLM response:\n{content}\n")

    # Remove markdown code fences (```json ... ``` or ``` ... ```)
    content_clean = re.sub(r"^```(?:json)?\s*", "", content, flags=re.MULTILINE)
    content_clean = re.sub(r"\s*```$", "", content_clean, flags=re.MULTILINE)
    content_clean = content_clean.strip()
    print(f"[DEBUG] After removing markdown:\n{content_clean}\n")

    parsed = None

    # Attempt 1: Direct JSON parse
    try:
        parsed = json.loads(content_clean)
        print("[DEBUG] Successfully parsed JSON directly")
    except json.JSONDecodeError as e:
        print(f"[DEBUG] Direct parse failed: {e}")
        
        # Attempt 2: Find JSON array using regex
        match = re.search(r"\[[\s\S]*\]", content_clean)
        if match:
            json_str = match.group(0)
            print(f"[DEBUG] Extracted JSON from content:\n{json_str}\n")
            try:
                parsed = json.loads(json_str)
                print("[DEBUG] Successfully parsed extracted JSON")
            except json.JSONDecodeError as e2:
                print(f"[DEBUG] Extracted JSON parse failed: {e2}")

    # Fallback: Return empty list if parsing completely failed
    if parsed is None:
        print("[DEBUG] All parsing attempts failed, returning empty list")
        return []

    # Handle dict response (keys are the action items)
    if isinstance(parsed, dict):
        print(f"[DEBUG] Parsed is a dict with keys: {list(parsed.keys())}")
        items = list(parsed.keys())
    # Handle list response
    elif isinstance(parsed, list):
        print(f"[DEBUG] Parsed is a list with {len(parsed)} items")
        items = parsed
    else:
        print(f"[DEBUG] Parsed value is neither dict nor list, got {type(parsed)}: {parsed}")
        return []

    # Extract and clean string items
    cleaned_items: list[str] = []
    for idx, value in enumerate(items):
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                cleaned_items.append(cleaned)
            else:
                print(f"[DEBUG] Skipped empty string at index {idx}")
        else:
            print(f"[DEBUG] Skipped non-string value at index {idx}: {type(value)} = {value}")

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for item in cleaned_items:
        key = item.lower()
        if key in seen:
            print(f"[DEBUG] Skipped duplicate: {item}")
            continue
        seen.add(key)
        unique.append(item)

    print(f"[DEBUG] Final extracted items: {unique}")
    return unique
