"""
AI 内容加工引擎
- 新闻摘要
- 情绪分析（利好/利空/中性）
- 智能标签（行业、板块、个股）
"""
import json
from typing import Optional

from loguru import logger
from openai import AsyncOpenAI

from app.core.config import settings


class AIProcessor:
    """使用 LLM 进行新闻内容语义加工"""

    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None

    def _get_client(self) -> AsyncOpenAI:
        if self.client is None:
            if not settings.LLM_API_KEY:
                raise ValueError("LLM_API_KEY is not configured")
            self.client = AsyncOpenAI(
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_BASE_URL,
            )
        return self.client

    async def process_news(
        self,
        title: str,
        content: str = "",
    ) -> dict:
        """
        综合处理一条新闻，返回:
        {
            "summary": "2-3句话摘要",
            "sentiment": "positive|negative|neutral",
            "sentiment_score": 0.8,  # -1.0 ~ 1.0
            "tags": ["科技", "AI"],
            "sectors": ["半导体", "消费电子"],
            "stocks": ["NVDA", "TSM"],
            "importance": 3  # 0-5
        }
        """
        try:
            client = self._get_client()

            prompt = f"""你是一个专业的财经新闻分析师。请分析以下新闻并以 JSON 格式返回结果。

标题: {title}
内容: {content[:2000] if content else '无正文'}

请返回严格的 JSON（不要 markdown 代码块），包含以下字段:
1. "summary": 用2-3句话概括核心信息
2. "sentiment": 对市场/投资的情绪判断，只能是 "positive"（利好）、"negative"（利空）、"neutral"（中性）之一
3. "sentiment_score": 情绪强度，-1.0（极度利空）到 1.0（极度利好），中性为0
4. "tags": 相关关键词标签数组，如 ["科技", "AI", "芯片"]
5. "sectors": 相关行业/板块数组，如 ["半导体", "新能源"]
6. "stocks": 相关股票代码数组（A股用代码如 "600519"，美股用 ticker 如 "AAPL"），无则空数组
7. "importance": 新闻重要性 0-5，0为不重要，5为极其重要（如央行降息、重大政策等）

只返回 JSON，不要任何其他文字。"""

            response = await client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )

            result_text = response.choices[0].message.content.strip()
            # 移除可能的 markdown 代码块标记
            if result_text.startswith("```"):
                result_text = result_text.split("\n", 1)[1]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]

            result = json.loads(result_text)
            return self._validate_result(result)

        except json.JSONDecodeError as e:
            logger.warning(f"AI 返回结果解析失败: {e}")
            return self._default_result()
        except ValueError:
            logger.warning("LLM API 未配置，跳过 AI 处理")
            return self._default_result()
        except Exception as e:
            logger.error(f"AI 处理失败: {e}")
            return self._default_result()

    async def summarize(self, title: str, content: str) -> str:
        """单独做摘要"""
        result = await self.process_news(title, content)
        return result.get("summary", "")

    async def analyze_sentiment(self, title: str, content: str = "") -> dict:
        """单独做情绪分析"""
        result = await self.process_news(title, content)
        return {
            "sentiment": result.get("sentiment", "neutral"),
            "sentiment_score": result.get("sentiment_score", 0.0),
        }

    @staticmethod
    def _validate_result(result: dict) -> dict:
        """校验和规范化 AI 返回结果"""
        validated = {
            "summary": str(result.get("summary", "")),
            "sentiment": result.get("sentiment", "neutral"),
            "sentiment_score": float(result.get("sentiment_score", 0.0)),
            "tags": list(result.get("tags", [])),
            "sectors": list(result.get("sectors", [])),
            "stocks": list(result.get("stocks", [])),
            "importance": int(result.get("importance", 0)),
        }

        # 确保 sentiment 在有效值范围内
        if validated["sentiment"] not in ("positive", "negative", "neutral"):
            validated["sentiment"] = "neutral"

        # 确保 importance 在 0-5 范围内
        validated["importance"] = max(0, min(5, validated["importance"]))

        # 确保 sentiment_score 在 -1.0 ~ 1.0 范围内
        validated["sentiment_score"] = max(-1.0, min(1.0, validated["sentiment_score"]))

        return validated

    @staticmethod
    def _default_result() -> dict:
        """默认结果（AI 不可用时）"""
        return {
            "summary": "",
            "sentiment": "neutral",
            "sentiment_score": 0.0,
            "tags": [],
            "sectors": [],
            "stocks": [],
            "importance": 0,
        }


# 全局单例
ai_processor = AIProcessor()
