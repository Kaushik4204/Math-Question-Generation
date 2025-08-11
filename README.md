# Math Question Generation
---
## Overview
This project automates the generation of math questions with structured tagging, image generation for questions, and exports the final output to a formatted Word document. It leverages Google Gemini API for generating questions and images, providing an efficient workflow for creating math quizzes or practice problems.
---

### Features
1.Generates math questions from a base JSON file using AI.

2.Parses tagged question strings into structured data.

3.Supports optional image generation per question.

4.Outputs questions into a well-formatted Word (.docx) document.

5.Ensures clean option lists, bolds correct answers, and provides explanations.
---
### Project Structure

math-question-generator/
│

├── data/                   # Base question files (JSON)


├── images/                 # Generated images for questions

├── output/                 # Output Word documents

├── src/                    # Source code modules

│   ├── generate_questions.py

│   ├── generate_images.py

│   ├── format_to_docx.py

│   ├── utils.py

│   └── config.py           # API key and configuration

├── main.py                 # Main script to run the pipeline

├── requirements.txt        # Python dependencies

├── .gitignore

└── README.md

## Setup Instructions

### Clone the repository

```bash
git clone https://github.com/Kaushik4204/Math-Question-Generation.git
cd Math-Question-Generation
Create and activate a Python virtual environment
```

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure your API key

Rename .env.example to .env (if you have one) or create a .env file in the root.

Add your Gemini API key:
GEMINI_API_KEY=your_api_key_here

Run the main script

```bash
python main.py

```

This will generate math questions, create images where required, and save a Word document in the output/ folder.
---

## Usage
Modify your base questions JSON file in the data/ folder to add or update question templates.

The pipeline handles generating questions and formatting them into a document automatically.

Check the images/ folder for any generated images linked to questions.

The final .docx report is stored under output/generated_questions.docx.
---

## Dependencies

google-generativeai — Gemini API Python client for generating questions and images.

python-docx — For creating and formatting Word documents.

python-dotenv — For managing environment variables (API keys).

requests — For HTTP requests (if needed).

regex — For regex operations.

---


## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or suggestions, please reach out to:

Kaushik Puli
GitHub: Kaushik4204
Email: your- kaushikpuli04@gmail.com
