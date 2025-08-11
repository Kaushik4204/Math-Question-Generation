import google.generativeai as genai
from src.config import GEMINI_API_KEY, MODEL_NAME
from src.utils import load_json
from typing import List

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

CURRICULUM_HIERARCHY = """
Use the curriculum hierarchy exactly as provided:
Quantitative Math 
Problem Solving
Numbers and Operations
Quantitative Math 
Problem Solving
Algebra
Quantitative Math 
Problem Solving
Geometry
Quantitative Math 
Problem Solving
Problem Solving
Quantitative Math 
Problem Solving
Probability and Statistics
Quantitative Math 
Problem Solving
Data Analysis
Quantitative Math 
Algebra
Algebraic Word Problems
Quantitative Math 
Algebra
Interpreting Variables
Quantitative Math 
Algebra
Polynomial Expressions (FOIL/Factoring)
Quantitative Math 
Algebra
Rational Expressions
Quantitative Math 
Algebra
Exponential Expressions (Product rule, negative exponents)
Quantitative Math 
Algebra
Quadratic Equations & Functions (Finding roots/solutions, graphing)
Quantitative Math 
Algebra
Functions Operations
Quantitative Math 
Geometry and Measurement
Area & Volume
Quantitative Math 
Geometry and Measurement
Perimeter
Quantitative Math 
Geometry and Measurement
Lines, Angles, & Triangles
Quantitative Math 
Geometry and Measurement
Right Triangles & Trigonometry
Quantitative Math 
Geometry and Measurement
Circles (Area, circumference)
Quantitative Math 
Geometry and Measurement
Coordinate Geometry
Quantitative Math 
Geometry and Measurement
Slope
Quantitative Math 
Geometry and Measurement
Transformations (Dilating a shape)
Quantitative Math 
Geometry and Measurement
Parallel & Perpendicular Lines
Quantitative Math 
Geometry and Measurement
Solid Figures (Volume of Cubes)
Quantitative Math 
Numbers and Operations
Basic Number Theory
Quantitative Math 
Numbers and Operations
Prime & Composite Numbers
Quantitative Math 
Numbers and Operations
Rational Numbers
Quantitative Math 
Numbers and Operations
Order of Operations
Quantitative Math 
Numbers and Operations
Estimation
Quantitative Math 
Numbers and Operations
Fractions, Decimals, & Percents
Quantitative Math 
Numbers and Operations
Sequences & Series
Quantitative Math 
Numbers and Operations
Computation with Whole Numbers
Quantitative Math 
Numbers and Operations
Operations with Negatives
Quantitative Math 
Data Analysis & Probability
Interpretation of Tables & Graphs
Quantitative Math 
Data Analysis & Probability
Trends & Inferences
Quantitative Math 
Data Analysis & Probability
Probability (Basic, Compound Events)
Quantitative Math 
Data Analysis & Probability
Mean, Median, Mode, & Range
Quantitative Math 
Data Analysis & Probability
Weighted Averages
Quantitative Math 
Data Analysis & Probability
Counting & Arrangement Problems
Quantitative Math 
Reasoning
Word Problems
"""

def generate_question(base_question: str) -> str:
    """
    Generates a new math question based on the base question using Gemini API.
    Output must follow exact tagged format.
    """
    prompt = f"""
You are given this base math question:

{base_question.strip()}

Task:
- Create a new question with the SAME difficulty & format.
- Change the context and numbers, but keep the structure.
- Preserve LaTeX formulas if any.
- Provide a new image description if the question requires an image.
- Output in EXACTLY the following Question Output Format without any extra text or explanation:

@title <Assessment title>
@description <Assessment description>

@question <Write your question here>
@instruction <Write instruction here>
@difficulty <easy|moderate|hard>
@subject <Choose subject from curriculum>
@unit <Choose unit from curriculum>
@topic <Choose topic from curriculum>
@plusmarks 1

@option <Option 1>
@option <Option 2>
@@option <Correct Option>
@option <Option 4>

@explanation <Write your question explanation here>

{CURRICULUM_HIERARCHY}

Remember: NO extra commentary or explanation outside the tagged format.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating question: {e}")
        return ""

def batch_generate(input_file: str) -> List[str]:
    """Generate questions for all base questions in a file."""
    base_questions = load_json(input_file)
    return [generate_question(q) for q in base_questions]

if __name__ == "__main__":
    new_questions = batch_generate("data/base_questions.json")
    for idx, q in enumerate(new_questions, 1):
        print(f"--- Question {idx} ---\n{q}\n")
