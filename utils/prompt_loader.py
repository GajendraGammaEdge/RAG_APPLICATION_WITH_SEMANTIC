from pathlib import Path

PROMPT_DIR = Path("prompts")


def load_prompt(prompt_name: str, **kwargs) -> str:
    prompt_path = PROMPT_DIR / prompt_name

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()

    return prompt_template.format(**kwargs)
