from openai import OpenAI
from config import settings
import re

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_blog_post(self, topic: str, length: str = "medium") -> str:
        prompt = f"""
        Write a professional blog post about {topic}.
        Keep it {length}.
        Use simple language and proper formatting.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return self.clean_output(response.choices[0].message.content)


    def generate_social_posts(self, topic: str, platform: str = "linkedin") -> list:
        posts = []

        for _ in range(3):
            prompt = f"""
            Write a high-quality {platform} post about {topic}.

            Requirements (MANDATORY):
            - Include a song name
            - Include singer name
            - Do NOT include any links or URLs
            - Do NOT include code
            - Use simple, clean English

            Platform-specific rules:

            If platform is LinkedIn:
            - Professional tone
            - Add 2–3 bullet points
            - Add insight or value
            - End with 3–5 relevant hashtags

            If platform is Instagram:
            - Focus on reel-style content
            - Add emotional or vibe-based language
            - Include 1–2 emojis
            - Keep it engaging and trendy
            - Add 5–8 hashtags

            If platform is Twitter:
            - Keep it very short (max 2–3 lines)
            - Make it catchy and impactful
            - No bullet points
            - Add 2–3 hashtags

            Format:
            Song: <song name>
            Singer: <singer name>

            Post:
            <final post>
            """

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            text = response.choices[0].message.content
            posts.append(self.clean_output(text))            

        return posts
    
    def clean_output(self, text):
        # remove URLs
        text = re.sub(r"http\S+", "", text)

        # remove weird code
        text = re.sub(r"[^\x00-\x7F]+", "", text)

        return text.strip()