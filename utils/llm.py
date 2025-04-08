import os
from dotenv import load_dotenv
from groq import Groq
from utils import logger

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@logger.catch
def generate_podcast_script(topic: str, content: str, duration: int = 5) -> str:
    """
    Generate a podcast script using Groq's LLaMA 3 model – base + expanded.
    """

    # Step 1: Generate base script
    base_prompt = f"""
You are a podcast host giving a solo monologue episode about the topic: "{topic}".

Write a clean, casual podcast script that lasts around 5-6 minutes (~600-700 words).
Keep it natural and engaging — like a friendly radio host speaking alone.

Avoid any scene directions like [pause], or labels like "Host:".
Just pure, natural dialogue.

Use the info below to guide your content:
\"\"\"{content}\"\"\"
"""

    try:
        logger.info("Generating base script with Groq...")
        base_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": base_prompt.strip()}],
            model="llama3-70b-8192",
            temperature=0.8,
            max_tokens=4096,
        )

        base_script = base_completion.choices[0].message.content

        # Step 2: Expand the script further
        expand_prompt = f"""
You are an expert podcast scriptwriter. Here's a podcast monologue:

\"\"\"{base_script}\"\"\"

Expand this script to be around 2000–4000 words. 
Keep the tone casual, fun, and informative — like a solo podcast host.
Don’t change the original style — just build on it and add more insights, examples, and natural flow.
"""

        logger.info("Expanding script with Groq...")
        expanded_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": expand_prompt.strip()}],
            model="llama3-70b-8192",
            temperature=0.75,
            max_tokens=8192
        )

        final_script = expanded_completion.choices[0].message.content
        return final_script

    except Exception as e:
        logger.critical(f"Groq-based podcast generation failed: {e}")
        return ""
