import json
import os
import re
from typing import Any, List, Dict


def load_json(filepath: str) -> Any:
    """
    Load JSON data from a file.
    
    Args:
        filepath (str): Path to the JSON file.
    
    Returns:
        Any: Parsed JSON content.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"JSON file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, filepath: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data (Any): Data to save.
        filepath (str): Path to the JSON file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Ensure directory exists
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse_tagged_questions(raw_questions: List[str]) -> List[Dict]:
    """
    Parses a list of raw question strings (in tagged format)
    into structured dictionaries.
    
    Args:
        raw_questions: List of question strings, each containing tagged fields.
    
    Returns:
        List of dicts representing parsed questions with keys:
        title, description, question, instruction, difficulty, subject,
        unit, topic, plusmarks, options, answer, explanation.
    """
    parsed_questions = []

    tag_re = re.compile(r'^@(\w+)\s+(.*)$')
    option_re = re.compile(r'^@(@)?option\s+(.*)$', re.IGNORECASE)

    for raw in raw_questions:
        qdict = {
            "title": "",
            "description": "",
            "question": "",
            "instruction": "",
            "difficulty": "",
            "subject": "",
            "unit": "",
            "topic": "",
            "plusmarks": "1",
            "options": [],
            "answer": "",
            "explanation": ""
        }

        lines = raw.strip().splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Match options first to handle correct answer
            m_opt = option_re.match(line)
            if m_opt:
                correct_flag = m_opt.group(1)
                opt_text = m_opt.group(2).strip()
                qdict["options"].append(opt_text)
                if correct_flag == "@":
                    qdict["answer"] = opt_text
                continue

            # Match other tags
            m = tag_re.match(line)
            if m:
                tag = m.group(1).lower()
                val = m.group(2).strip()
                if tag in qdict:
                    qdict[tag] = val
                else:
                    # Unknown tags are ignored
                    pass

        parsed_questions.append(qdict)

    return parsed_questions
