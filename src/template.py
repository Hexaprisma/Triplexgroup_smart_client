class PromptTemplate:
    def __init__(self):
        self.base_template = """A conversation between User and Assistant. The user asks a question, and the Assistant solves it.
The assistant first thinks about the reasoning process in the mind and then provides the user with the answer.
The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively.

User: {question}
Assistant: {think_tag}
{reasoning}
{think_end_tag}
{answer_tag}
{solution}
{answer_end_tag}
"""

    def generate_math_prompt(self, question):
        """Generate a prompt for mathematical problems"""
        return self.base_template.format(
            question=question,
            think_tag="<think>",
            reasoning="""1. First, let's understand what the question is asking
2. Break down the mathematical components
3. Apply relevant mathematical rules
4. Calculate step by step
5. Verify the result""",
            think_end_tag="</think>",
            answer_tag="<answer>",
            solution="[Mathematical solution will be provided here]",
            answer_end_tag="</answer>"
        )

    def generate_code_prompt(self, question):
        """Generate a prompt for coding problems"""
        return self.base_template.format(
            question=question,
            think_tag="<think>",
            reasoning="""1. Analyze the programming requirements
2. Consider edge cases and constraints
3. Plan the algorithm structure
4. Think about time and space complexity
5. Consider test cases""",
            think_end_tag="</think>",
            answer_tag="<answer>",
            solution="[Code solution will be provided here]",
            answer_end_tag="</answer>"
        )

# Example usage
if __name__ == "__main__":
    template = PromptTemplate()
    
    # Example 1: Math Problem
    math_question = "Calculate the area of a circle with radius 5 units."
    math_prompt = template.generate_math_prompt(math_question)
    print("Math Problem Template:")
    print("-" * 50)
    print(math_prompt)
    print("\n")
    
    # Example 2: Code Problem
    code_question = "Write a function to find the factorial of a number."
    code_prompt = template.generate_code_prompt(code_question)
    print("Code Problem Template:")
    print("-" * 50)
    print(code_prompt)

# Example outputs would look like:
"""
Example 1 - Math Problem:
User: Calculate the area of a circle with radius 5 units.
Assistant: <think>
1. First, let's understand what the question is asking
2. Break down the mathematical components
3. Apply relevant mathematical rules
4. Calculate step by step
5. Verify the result
</think>
<answer>
Let's solve this step by step:
1. Area of circle = π * r²
2. r = 5 units
3. Area = π * 5²
4. Area = π * 25
5. Area ≈ 78.54 square units
</answer>

Example 2 - Code Problem:
User: Write a function to find the factorial of a number.
Assistant: <think>
1. Analyze the programming requirements
2. Consider edge cases and constraints
3. Plan the algorithm structure
4. Think about time and space complexity
5. Consider test cases
</think>
<answer>
def factorial(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    return n * factorial(n-1)
</answer>
"""