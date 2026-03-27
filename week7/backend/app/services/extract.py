import re


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[str] = []
    date_pattern = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

    for line in lines:
        normalized = line.lower()
        if normalized.startswith("todo:") or normalized.startswith("action:"):
            results.append(line)
        elif line.endswith("!"):
            results.append(line)

        # Extract ISO-like dates from each line, e.g., 2026-03-27.
        results.extend(date_pattern.findall(line))

    # Deduplicate while preserving order.
    return list(dict.fromkeys(results))


