from core.settings import BASE_DIR

PROMPTS_DIR = BASE_DIR / "main" / "prompts"

LEGAL_ADVISOR_PROMPT = open(PROMPTS_DIR / "base_prompt.txt").read()

