"""AI Services with mock LLM functions"""
from typing import List, Dict, Any
import json
import logging
import os
import re

import httpx


class MockLLMService:
    """Mock LLM service for testing without API keys"""

    @staticmethod
    def explain_text(text: str, context: str = None) -> Dict[str, Any]:
        """Generate explanation for selected text"""
        explanation_map = {
            "epistemology": "认识论，研究知识的来源、本质和范围的哲学分支。涉及人如何获取知识、验证知识的真伪。",
            "hermeneutics": "解释学，关于理解和解释文本、历史、文化意义的方法论。强调语境和解释者的前理解对意义构成的影响。",
            "phenomenology": "现象学，专注于意识现象和主观体验的哲学方向。研究人类如何经历和理解世界。",
            "synthesis": "综合，结合不同观点或信息创造新的整体理解。在学术写作中表示融合多个来源的思想。",
            "discourse": "话语、论述，指特定领域的对话、观点体系或叙述方式。文化话语涉及社会共同的理解框架。",
        }

        # Check for keywords and provide explanations
        lower_text = text.lower()
        explanation = None
        key_terms = []

        for term, expl in explanation_map.items():
            if term in lower_text:
                explanation = expl
                key_terms.append(term)

        if not explanation:
            explanation = f"'{text}' 是一个学术概念。它通常在以下语境中使用：{context or '学术研究和理论讨论'} 相关。建议查阅相关学术文献以获得更深入的理解。"

        return {
            "original_text": text,
            "explanation": explanation,
            "key_terms": key_terms or ["学术概念", "理论"],
        }

    @staticmethod
    def generate_essay_ideas(paper_title: str, abstract: str = None) -> List[str]:
        """Generate essay ideas based on paper"""
        ideas = [
            f"论文'{paper_title}'的理论框架对现代教育的影响",
            f"从'{paper_title}'的角度探讨中文学术写作的未来发展",
            f"批判性分析：'{paper_title}'中存在的局限性与改进空间",
            f"'{paper_title}'与传统中文学术传统的对话与融合",
            f"如何将'{paper_title}'的核心观点应用于实际研究",
        ]
        return ideas[:3]  # Return top 3 ideas

    @staticmethod
    def humanise_writing(text: str) -> str:
        """Make academic writing more natural and readable"""
        replacements = {
            "鉴于": "考虑到",
            "此外": "另外",
            "就": "关于",
            "而言": "来说",
            "相应地": "因此",
            "故": "所以",
            "由此可见": "由此可知",
        }

        humanised = text
        for formal, natural in replacements.items():
            humanised = humanised.replace(formal, natural)

        # Add more natural sentence structure suggestions
        if len(humanised) > 100:
            humanised = humanised.replace("，", "。") if "。" in humanised else humanised

        return humanised

    @staticmethod
    def find_chinese_quotes(keyword: str) -> List[Dict[str, str]]:
        """Find Chinese classical quotes related to keyword"""
        quote_db = [
            {
                "quote": "学而时习之，不亦说乎",
                "source": "《论语》",
                "author": "孔子",
                "era": "春秋战国",
                "meaning": "学习了知识，经常复习它，不是很快乐吗？强调学习与实践的结合。",
                "keywords": ["学习", "修养", "孔子"],
            },
            {
                "quote": "知己知彼，百战不殆",
                "source": "《孙子兵法》",
                "author": "孙武",
                "era": "春秋战国",
                "meaning": "了解自己和敌人，就不会在战争中失利。引申为全面理解问题。",
                "keywords": ["知识", "策略", "理解"],
            },
            {
                "quote": "纸上得来终觉浅，绝知此事要躬行",
                "source": "《冬夜读书示子聿》",
                "author": "陆游",
                "era": "南宋",
                "meaning": "从书本上获得的知识终究很肤浅，要真正理解还需亲身体验。",
                "keywords": ["理论", "实践", "学习"],
            },
            {
                "quote": "读书破万卷，下笔如有神",
                "source": "《奉赠韦左丞丈》",
                "author": "杜甫",
                "era": "唐代",
                "meaning": "阅读大量书籍，写文章就像有神灵相助。强调阅读量对写作的影响。",
                "keywords": ["阅读", "写作", "学问"],
            },
            {
                "quote": "君子之学，贵以专",
                "source": "《荀子》",
                "author": "荀子",
                "era": "春秋战国",
                "meaning": "君子的学习，贵在专注。强调学习的专注性和深度。",
                "keywords": ["学习", "专注", "修养"],
            },
        ]

        lower_keyword = keyword.lower()
        results = []

        for quote in quote_db:
            # Check if keyword matches any field
            if (
                lower_keyword in quote["quote"].lower()
                or lower_keyword in quote["author"].lower()
                or lower_keyword in quote["source"].lower()
                or any(lower_keyword in k.lower() for k in quote["keywords"])
            ):
                results.append(
                    {
                        "quote": quote["quote"],
                        "source": quote["source"],
                        "author": quote["author"],
                        "era": quote["era"],
                        "meaning": quote["meaning"],
                    }
                )

        # If no exact match, return relevant quotes
        if not results:
            results = quote_db[:2]

        return results

    @staticmethod
    def translate_text(text: str, target_language: str = "en") -> str:
        """Mock translation"""
        return f"[Mock Translate -> {target_language}] {text}"


logger = logging.getLogger("ai_service")


class AIService:
    """AI Service - uses mock LLM by default, can be extended with real API"""

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock_service = MockLLMService()

    def _groq_chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY")

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        with httpx.Client(timeout=25.0) as client:
            response = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

    def explain_text(self, text: str, context: str = None) -> Dict[str, Any]:
        """Wrapper for text explanation"""
        if self.use_mock:
            return self.mock_service.explain_text(text, context)

        logger.info("Explain via Groq")

        prompt = (
            "你是中文学术阅读助手。请基于常识性知识解释所选文本，"
            "不进行网络搜索，不虚构引用。"
            "优先输出JSON，键为: original_text, explanation, key_terms。"
            "explanation为中文解释，100-200字为宜，避免在解释中使用英文双引号。"
            "key_terms为3-6个关键词数组。"
            "如果无法输出JSON，请按以下格式输出三行：\n"
            "ORIGINAL_TEXT: ...\nEXPLANATION: ...\nKEY_TERMS: term1, term2, term3"
        )
        user_payload = {
            "text": text,
            "context": context or "",
        }

        try:
            content = self._groq_chat(
                [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
                ],
                temperature=0.3,
            )
        except (httpx.HTTPError, KeyError, ValueError):
            return self.mock_service.explain_text(text, context)

        parsed = None
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", content)
            if match:
                try:
                    parsed = json.loads(match.group(0))
                except json.JSONDecodeError:
                    parsed = None

        if isinstance(parsed, dict):
            return {
                "original_text": parsed.get("original_text", text),
                "explanation": parsed.get("explanation", ""),
                "key_terms": parsed.get("key_terms", []),
            }

        raw = content.strip()
        if raw.startswith("ORIGINAL_TEXT:"):
            lines = [line.strip() for line in raw.splitlines() if line.strip()]
            original_line = next((l for l in lines if l.startswith("ORIGINAL_TEXT:")), "")
            explain_line = next((l for l in lines if l.startswith("EXPLANATION:")), "")
            terms_line = next((l for l in lines if l.startswith("KEY_TERMS:")), "")
            original = original_line.replace("ORIGINAL_TEXT:", "", 1).strip() or text
            explanation_text = explain_line.replace("EXPLANATION:", "", 1).strip()
            terms = terms_line.replace("KEY_TERMS:", "", 1).strip()
            key_terms = [t.strip() for t in terms.split(",") if t.strip()]
            return {
                "original_text": original,
                "explanation": explanation_text or raw,
                "key_terms": key_terms,
            }

        if '"explanation"' in raw and '"key_terms"' in raw:
            expl_start = raw.find('"explanation"')
            terms_start = raw.find('"key_terms"')
            explanation_chunk = raw[expl_start:terms_start]
            explanation_text = explanation_chunk.split(":", 1)[-1].strip().lstrip("\"").rstrip("\", \n\t")

            terms_chunk = raw[terms_start:]
            list_start = terms_chunk.find("[")
            list_end = terms_chunk.find("]")
            key_terms = []
            if list_start != -1 and list_end != -1 and list_end > list_start:
                list_body = terms_chunk[list_start + 1 : list_end]
                key_terms = [t.strip().strip("\"") for t in list_body.split(",") if t.strip()]

            return {
                "original_text": text,
                "explanation": explanation_text or raw,
                "key_terms": key_terms,
            }

        return {
            "original_text": text,
            "explanation": raw,
            "key_terms": [],
        }

    def generate_essay_ideas(self, paper_title: str, abstract: str = None) -> List[str]:
        """Wrapper for essay idea generation"""
        if self.use_mock:
            return self.mock_service.generate_essay_ideas(paper_title, abstract)
        return self.mock_service.generate_essay_ideas(paper_title, abstract)

    def humanise_writing(self, text: str) -> str:
        """Wrapper for writing humanization"""
        if self.use_mock:
            return self.mock_service.humanise_writing(text)
        return self.mock_service.humanise_writing(text)

    def find_chinese_quotes(self, keyword: str) -> List[Dict[str, str]]:
        """Wrapper for Chinese quote finding"""
        if self.use_mock:
            return self.mock_service.find_chinese_quotes(keyword)
        return self.mock_service.find_chinese_quotes(keyword)

    def translate_text(self, text: str, target_language: str = "en") -> str:
        """Translate text via Groq if available, else mock"""
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
        if not api_key:
            return self.mock_service.translate_text(text, target_language)

        if target_language.lower() in {"zh", "zh-cn", "zh-hans", "baihua", "modern-chinese"}:
            instruction = (
                "将以下文言文或古汉语翻译成白话文，保持意思准确、语气自然。"
                "只输出翻译结果。"
            )
        else:
            instruction = (
                "Translate the following text into English. Return only the translated text."
            )

        prompt = f"{instruction}\n\n{text}"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Return only the translation."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json=payload,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()
        except (httpx.HTTPError, KeyError):
            return self.mock_service.translate_text(text, target_language)

    def extract_pdf_metadata(self, text: str) -> Dict[str, Any]:
        """Extract PDF metadata with Groq if API key exists, else return empty dict"""
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
        if not api_key or not text.strip():
            return {}

        prompt = (
            "You are extracting metadata from a Chinese academic paper. "
            "Return JSON only with keys: title, author, year, abstract. "
            "Use empty string if missing. Text:\n\n"
            f"{text[:6000]}"
        )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Return JSON only. No extra text."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json=payload,
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                return json.loads(content)
        except (httpx.HTTPError, KeyError, json.JSONDecodeError):
            return {}


# Global AI service instance
_has_groq_key = bool(os.getenv("GROQ_API_KEY", "").strip())
ai_service = AIService(use_mock=not _has_groq_key)
logger.info("AI service mode: %s", "groq" if _has_groq_key else "mock")
print(f"AI service mode: {'groq' if _has_groq_key else 'mock'}")
