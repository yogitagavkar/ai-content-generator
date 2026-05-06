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
            Write a high-quality {platform} post about: {topic}

                General Rules:
                - Use simple, clean English
                - Do NOT include any links or URLs
                - Do NOT include code
                - Keep content relevant to topic

                Content Rules:

                If the topic is about music / songs:
                - Include:
                Song: <song name>
                Singer: <singer name>

                If the topic is about news, crime, or sensitive issues:
                - DO NOT include song or singer
                - Use respectful and serious tone
                - Focus on awareness, empathy, or facts
                - Avoid exaggeration

                Platform Rules:

                If platform is LinkedIn:
                - Professional tone
                - Add 2–3 bullet points
                - Add 3–5 hashtags

                If platform is Instagram:
                - Emotional + engaging tone
                - Use 1–2 emojis (only if appropriate)
                - Add 5–8 hashtags

                If platform is Twitter:
                - Very short (2–3 lines)
                - No bullet points
                - Add 2–3 hashtags

                Output Format:

                If music topic:
                Song: <name>
                Singer: <name>

                Post:
                <content>

                If NOT music topic:
                Post:
                <content>
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