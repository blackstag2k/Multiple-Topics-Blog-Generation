import google.genai as genai
import pandas as pd
import json
import time
client = genai.Client(api_key="ENTER_API_KEY")

df = pd.read_csv(r"C:\Users\Bhaskar Rana\OneDrive\Desktop\topics.csv")
topic_list = df.iloc[0:3, 0]. to_list()

def generate_outline(topic):
    prompt = f"""
[SYSTEM INSTRUCTION]
You are an expert blog post outlining tool. Your task is to generate a comprehensive, yet highly concise, outline for a single blog post. The final blog post must have an approximate total length of 300 words. Therefore, the outline must be tight and focus only on the most essential points.

Your output must strictly follow this structure:
1. **Title:** A compelling, SEO-friendly title (7-10 words).
2. **Word Count Goal:** [300 words] (fixed).
3. **Introduction (approx. 50 words):** A two-sentence hook and thesis statement.
4. **Main Points (approx. 200 words total):** A maximum of three sub-sections (H2/H3 level). Each sub-section should have a headline and 2-3 bullet points detailing the specific content to be covered.
5. **Conclusion (approx. 50 words):** A summary sentence and a single, strong call-to-action (CTA).
6. **Tone:** [Specify the appropriate tone for the topic, e.g., Informative and Encouraging]

[USER QUERY]
Please generate a blog post outline following the [SYSTEM INSTRUCTION]. The specific topic is: "{topic}"
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

def generate_blog(outline):
    prompt = f"""
[SYSTEM INSTRUCTION]
You are a professional content writer. Your task is to transform the provided outline into a complete, polished blog post.

**STRICT CONSTRAINTS:**
1. **Total Length:** The final output **must not exceed 300 words**. Be concise and prioritize impact over detail.
2. **Structure:** Adhere strictly to the structure, titles, and points laid out in the provided outline.
3. **Formatting:** Use appropriate headings (e.g., **Introduction**, **H2 Headlines**) and paragraph breaks for readability. Do not include the 'Word Count Goal' or other planning notes in the final post.

[USER QUERY]
Please generate the final blog post content, strictly following the system instructions and utilizing the provided outline: {outline}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

def generate_critique(blog):
    prompt = f"""
[SYSTEM INSTRUCTION]
You are a highly analytical content editor and critic. Your task is to provide a comprehensive, constructive critique of the provided blog post. Your analysis must be structured and focus on three key areas: Constraints, Content Quality, and Suggestions.

Your output must strictly follow this structure:

## 🔍 Blog Post Critique
---
### 1. Constraint Check (Strict Adherence)
* **Word Count:** State the estimated word count and confirm if it adheres to the **300-word limit**. (Pass/Fail)
* **Structure & Flow:** Did the post strictly follow the required Introduction-Main Points-Conclusion structure? (Yes/No)
* **Tone:** Was the tone appropriate and consistent throughout? (Yes/No)

### 2. Content Quality & Impact
* **Clarity:** Is the main idea immediately clear and easy to understand?
* **Engagement:** Is the title compelling, and does the introduction hook the reader effectively?
* **Conciseness:** Did the post utilize the limited word count effectively, avoiding unnecessary jargon or filler? (Provide one specific example of a strong/weak sentence.)

### 3. Actionable Suggestions (Maximum 2 Points)
* Provide 1-2 specific, actionable suggestions to improve the post's impact, clarity, or SEO value, while *still* respecting the 300-word limit.

[USER QUERY]
Please generate a structured critique using the [SYSTEM INSTRUCTION] for the following blog post content: {blog}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

output = []

for topic in topic_list:

    outline = generate_outline(topic)
    blog = generate_blog(outline)
    critique = generate_critique(blog)

    blog_content = {
    "topic": topic,
    "outline": outline,
    "blog": blog,
    "critique": critique
    }

    output.append(blog_content)

    file = topic + ".json"
    with open(file, "w", encoding = "utf-8")as f:
        json.dump(blog_content, f, indent=4, ensure_ascii=False)

    print(f"Saved {file}")

    time.sleep(6)