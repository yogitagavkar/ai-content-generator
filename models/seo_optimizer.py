import re
from html import unescape


class SEOOptimizer:
    def clean_text(self, text: str) -> str:
        text = unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def generate_slug(self, title: str) -> str:
        title = self.clean_text(title).lower()
        title = re.sub(r"[^a-z0-9\s-]", "", title)
        title = re.sub(r"\s+", "-", title)
        title = re.sub(r"-+", "-", title)
        return title.strip("-")

    def generate_meta_title(self, title: str, max_length: int = 60) -> str:
        title = self.clean_text(title)
        return title[:max_length].rstrip()

    def generate_meta_description(self, content: str, max_length: int = 160) -> str:
        content = self.clean_text(content)
        if len(content) <= max_length:
            return content
        truncated = content[:max_length].rsplit(" ", 1)[0]
        return truncated + "..."

    def extract_keywords(self, content: str, top_n: int = 10):
        stop_words = {
            "the", "is", "in", "and", "to", "of", "a", "for", "on", "with",
            "that", "as", "by", "an", "are", "at", "from", "or", "be", "this",
            "it", "your", "you", "we", "can", "our"
        }

        words = re.findall(r"\b[a-zA-Z]{3,}\b", content.lower())
        filtered = [word for word in words if word not in stop_words]

        freq = {}
        for word in filtered:
            freq[word] = freq.get(word, 0) + 1

        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:top_n]]

    def optimize(self, title: str, content: str) -> dict:
        return {
            "slug": self.generate_slug(title),
            "meta_title": self.generate_meta_title(title),
            "meta_description": self.generate_meta_description(content),
            "keywords": self.extract_keywords(content),
        }