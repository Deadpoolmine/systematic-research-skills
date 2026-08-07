#!/usr/bin/env python3
"""
Category Manager — create and list knowledge categories.

Usage:
    python create-category.py --list              List allowed categories
    python create-category.py <name>              Create a new category
    python create-category.py --add <name>        Add to allowed list
    python create-category.py --output <dir>      Set knowledge root (default: knowledge/)
"""

import sys
import os
import json
from pathlib import Path

# Default allowed categories — constrained list
DEFAULT_CATEGORIES = [
    "finance",
    "market",
    "technology",
    "science",
    "policy",
    "industry",
    "healthcare",
    "energy",
    "education",
    "law",
]

CATEGORY_NAMES = {
    "finance": "Finance & Economics",
    "market": "Market Analysis",
    "technology": "Technology & Engineering",
    "science": "Scientific Research",
    "policy": "Policy & Regulation",
    "industry": "Industry & Manufacturing",
    "healthcare": "Healthcare & Medicine",
    "energy": "Energy & Environment",
    "education": "Education & Training",
    "law": "Law & Governance",
}


def load_config(root: str) -> dict:
    """Load or create category config."""
    config_path = os.path.join(root, ".categories.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"allowed": list(DEFAULT_CATEGORIES)}


def save_config(root: str, config: dict):
    """Save category config."""
    os.makedirs(root, exist_ok=True)
    config_path = os.path.join(root, ".categories.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def create_category(name: str, root: str):
    """Create category directory and index.md."""
    cat_dir = os.path.join(root, name)
    os.makedirs(cat_dir, exist_ok=True)

    display = CATEGORY_NAMES.get(name, name.replace("-", " ").title())
    index_path = os.path.join(cat_dir, "index.md")
    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(f"# {display}\n\n")
            f.write(f"Research items in the {display} category.\n\n")
            f.write("## Items\n\n")
        print(f"Created {index_path}")
    else:
        print(f"Category exists: {index_path}")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    knowledge_root = "knowledge"

    # Parse --output
    filtered = []
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            knowledge_root = args[i + 1]
            i += 2
        else:
            filtered.append(args[i])
            i += 1

    config = load_config(knowledge_root)

    if filtered[0] == "--list":
        print("Allowed categories:")
        for c in config["allowed"]:
            display = CATEGORY_NAMES.get(c, c)
            exists = os.path.isdir(os.path.join(knowledge_root, c))
            marker = " [exists]" if exists else ""
            print(f"  {c} — {display}{marker}")

    elif filtered[0] == "--add" and len(filtered) > 1:
        name = filtered[1].lower().replace(" ", "-")
        if name not in config["allowed"]:
            config["allowed"].append(name)
            config["allowed"].sort()
            save_config(knowledge_root, config)
            print(f"Added '{name}' to allowed categories.")
        else:
            print(f"'{name}' already in allowed list.")
        create_category(name, knowledge_root)

    else:
        name = filtered[0].lower().replace(" ", "-")
        if name not in config["allowed"]:
            print(f"ERROR: '{name}' is not in the allowed categories list.")
            print("Allowed categories:")
            for c in config["allowed"]:
                print(f"  {c}")
            print(f"\nUse --add {name} to add it, or choose from the list above.")
            sys.exit(1)

        create_category(name, knowledge_root)

        # Ensure root index.md exists
        root_index = os.path.join(knowledge_root, "index.md")
        if not os.path.exists(root_index):
            with open(root_index, "w", encoding="utf-8") as f:
                f.write("---\nokf_version: \"0.2\"\n---\n\n")
                f.write("# Knowledge Bundle\n\n")
                f.write("Systematic research knowledge base.\n\n")
                f.write("## Categories\n\n")
            print(f"Created root {root_index}")
        else:
            print(f"Root index exists: {root_index}")


if __name__ == "__main__":
    main()
