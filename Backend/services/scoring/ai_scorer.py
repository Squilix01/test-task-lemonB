import logging
import httpx
from typing import Tuple
from settings.config import config
import re
import math

#logger = logging.getLogger(__name__)

class ProductScorer:
    def __init__(self):
        self.llm_provider = config.llm.provider
        self.api_key = config.llm.api_key
        self.model_name = config.llm.model_name 

    def _fallback_score(self, rating: float, reviews: int, trend_score: float, boost_score: float) -> Tuple[int, str]:

        # 1. Рейтингові бали в реальному діапазоні [3.0 - 5.0] (до 25 балів)
        rating_pts = max(0.0, (rating - 3.0) / 2.0) * 25.0
        
        # 2. Logarithmic review scaling up to 50,000 reviews (up to 25 pts)
        if reviews > 0:
            reviews_pts = min(math.log10(max(reviews, 1)) / math.log10(50000), 1.0) * 25.0
        else:
            reviews_pts = 0.0

        # 3. Trend momentum points (up to 25 pts)
        trend_val = trend_score if trend_score is not None else 65.0
        trend_pts = (trend_val / 100.0) * 25.0

        # 4. Sales Boost points (up to 25 pts)
        boost_pts = min(boost_score if boost_score is not None else 0.0, 25.0)

        raw_score = rating_pts + reviews_pts + trend_pts + boost_pts
        final_score = int(min(max(raw_score, 1), 99))

        reviews_fmt = f"{reviews / 1000:.1f}k" if reviews >= 1000 else str(reviews)
        reasoning = (
            f"Товар демонструє стабільний комерційний потенціал {final_score}/100 за аналітичною моделлю.\n"
            f"• Якість товару: рейтинг {rating:.1f}/5 дає {rating_pts:.1f} із 25 балів.\n"
            f"• Попит та соціальний доказ: {reviews_fmt} відгуків додають {reviews_pts:.1f} із 25 балів.\n"
            f"• Динаміка інтересу: Google Trends індекс ({trend_val:.0f}/100) додає {trend_pts:.1f} балів.\n"
            f"• Sales Boost бонус: +{boost_pts:.1f} балів за збіг з успішними продажами компанії."
        )
        return final_score, reasoning

    async def calculate_score(self, name: str, category: str, rating: float, reviews: int, trend_score: float, boost_score: float) -> Tuple[int, str]:
        if not self.llm_provider or not self.api_key:
            #logger.warning("LLM не налаштовано, використовується базова формула розрахунку.")
            return self._fallback_score(rating, reviews, trend_score, boost_score)

        try:
            prompt = (
                f"Ти провідний аналітик ринку e-Commerce та Amazon. "
                f"Твоє завдання — об'єктивно оцінити комерційний потенціал товару для баєра за шкалою від 1 до 100.\n\n"
                f"Метрики товару:\n"
                f"- Назва: {name}\n"
                f"- Категорія: {category}\n"
                f"- Рейтинг: {rating} / 5.0\n"
                f"- Кількість відгуків: {reviews}\n"
                f"- Показник інтересу в Google Trends: {trend_score} / 100\n"
                f"- Додатковий бонус історичних продажів (Sales Boost): +{boost_score} б.\n\n"
                f"Вимоги до оцінки:\n"
                f"1. Оцінка має бути динамічною та диференційованою (НЕ став усім одне й те саме число! Діапазон від 35 до 96).\n"
                f"2. Високий бал (80-96): товари-хіти з високим попитом, сильним брендом і високим рейтингом.\n"
                f"3. Середній бал (55-79): стабільні базові товари повсякденного попиту.\n"
                f"4. Низький бал (30-54): товари з надмірною конкуренцією або слабкою маржинальністю.\n"
                f"5. Формат відповіді: лише ЦІЛЕ ЧИСЛО (1-100), вертикальна риска '|', та 1-2 ємних речення українською мовою з професійним висновком для баєра.\n"
                f"Приклад формату: 88 | Високий попит та стабільна база відгуків свідчать про чудову ліквідність, а високий інтерес покупців мінімізує ризики залишків."
            )
            
            provider = self.llm_provider.lower()
            if provider == "openai":
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {
                    "model": self.model_name or "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                }
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, headers=headers, json=payload, timeout=12.0)
                    response.raise_for_status()
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
            elif provider == "gemini":
                model = self.model_name or "gemini-1.5-flash"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.3
                    }
                }
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=payload, timeout=12.0)
                    response.raise_for_status()
                    data = response.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                #logger.warning(f"Провайдер {self.llm_provider} не підтримується, використовується базова формула.")
                return self._fallback_score(rating, reviews, trend_score, boost_score)

            parts = content.strip().split("|")
            score_str = parts[0].strip().replace("Score:", "").replace("Оцінка:", "").strip()
            import re
            numbers = re.findall(r"\d+", score_str)
            score = int(numbers[0]) if numbers else 60
            reasoning = parts[1].strip() if len(parts) > 1 else content.strip()
            return min(max(score, 1), 99), reasoning
                
        except Exception as e:
            #logger.error(f"Помилка при зверненні до LLM: {e}")
            return self._fallback_score(rating, reviews, trend_score, boost_score)
