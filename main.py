import os
import re
import google.generativeai as genai

from src.generate_questions import batch_generate
from src.format_to_docx import save_questions_to_word
from src.generate_images import create_image
from src.config import GEMINI_API_KEY
from src.utils import parse_tagged_questions  # Make sure parse_tagged_questions is in utils.py

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

BASE_QUESTIONS_PATH = "data/base_questions.json"
OUTPUT_DOC_PATH = "output/generated_questions.docx"


def extract_image_prompts(raw_questions: list):
    """
    Extract (image_prompt, local_path) from each raw question's @image tag.
    Returns a list of tuples (prompt or None, path or None).
    """
    image_data = []
    for idx, raw_q in enumerate(raw_questions, 1):
        match = re.search(r'^@image\s+(.+)$', raw_q, re.MULTILINE)
        if match:
            prompt = match.group(1).strip()
            img_path = f"images/question{idx}.png"
            image_data.append((prompt, img_path))
        else:
            image_data.append((None, None))
    return image_data


if __name__ == "__main__":
    print("🚀 Starting Math Question Generation...")

    # 1. Check if base questions exist
    if not os.path.exists(BASE_QUESTIONS_PATH):
        print(f"❌ Error: Base questions file not found at {BASE_QUESTIONS_PATH}")
        exit(1)

    # 2. Generate new questions (list of raw tagged strings)
    print("📄 Generating new questions from base file...")
    raw_questions = batch_generate(BASE_QUESTIONS_PATH)

    if not raw_questions:
        print("⚠️ No questions were generated. Please check batch_generate function.")
        exit(1)

    print(f"✅ Generated {len(raw_questions)} questions.")
    print("🔍 Preview of first question:")
    print(raw_questions[0])

    # 3. Parse raw tagged question strings into structured dictionaries
    parsed_questions = parse_tagged_questions(raw_questions)

    # 4. Generate images for questions with @image tag
    os.makedirs("images", exist_ok=True)
    print("🖼 Creating images for questions that require them...")

    image_prompts = extract_image_prompts(raw_questions)
    for idx, (prompt, path) in enumerate(image_prompts, 1):
        if prompt and path:
            print(f"Generating image for Question {idx} with prompt: {prompt}")
            create_image(prompt, path)
        else:
            print(f"No image required for Question {idx}")

    print("✅ Images saved to images/ folder")

    # 5. Save parsed questions to Word document
    os.makedirs("output", exist_ok=True)
    save_questions_to_word(parsed_questions, OUTPUT_DOC_PATH)
    print(f"💾 Questions saved to: {OUTPUT_DOC_PATH}")

    print("\nAll tasks completed successfully!")
