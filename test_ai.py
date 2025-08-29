import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Configure AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Test texts with different issues
test_texts = [
    "how are we sad today",
    "this is not working properly and i dont know why",
    "The meeting will be tomorrow at 3pm dont forget",
    "I think this approach is better then the other one",
    "Can you help me with this problem its very urgent"
]

# Current prompt
def test_current_prompt(text):
    prompt = f"""You are a professional text editor agent. Your task is to improve the following text by:

1. Fixing grammar and spelling errors
2. Improving clarity and readability
3. Making it sound more natural
4. Preserving the original meaning and tone

Rules:
- Return ONLY the improved text
- No explanations, options, or additional commentary
- Keep the same length and style as the original
- If the text is already perfect, return it unchanged

Text to improve: "{text}"

Improved text:"""
    
    generation_config = {
        "temperature": 0.2,
        "max_output_tokens": max(len(text) + 50, 150),
        "top_p": 0.8
    }
    
    response = model.generate_content(prompt, generation_config=generation_config)
    return response.text.strip()

# Test all examples
print("=== TESTING CURRENT AI PROMPT ===\n")
for i, text in enumerate(test_texts, 1):
    print(f"Test {i}:")
    print(f"Original: '{text}'")
    result = test_current_prompt(text)
    print(f"AI Result: '{result}'")
    print(f"Length: {len(text)} -> {len(result)}")
    print("-" * 50)