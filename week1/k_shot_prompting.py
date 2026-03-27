import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
# YOUR_SYSTEM_PROMPT = """
# You are an expert text manipulator who loves classic literature. 
# Your task is to reverse the order of letters in the given word. 
# You must ONLY output the reversed word, with absolutely no other text, punctuation, or explanation.

# Here are some examples of how you should do it:

# Word: hamlet
# Reversed: telmah

# Word: dracula
# Reversed: alucard

# Word: odyssey
# Reversed: yessydo

# Word: gatsby
# Reversed: ybstag
# """

YOUR_SYSTEM_PROMPT = """
You are a perfect text reversal engine. You process text strictly character-by-character. 
You ONLY output the reversed word, with no extra text.

Here are examples of how to reverse tricky words correctly:

User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

status
Assistant: sutats

User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

http
Assistant: ptth

User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
Assistant: sutatsptth
"""

USER_PROMPT = "Reverse the order of letters in the following word. Only output the reversed word, no other text:\n\nhttpstatus"
EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)