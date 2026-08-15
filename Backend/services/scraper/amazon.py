import asyncio
import logging
import re
from typing import Any
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

logger = logging.getLogger(__name__)


class AmazonScraper:
    def __init__(self) -> None:
        self.base_url = "https://www.amazon.com/gp/bestsellers/"

    async def scrape_best_sellers(self, max_items: int = 50) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-infobars",
                        "--window-position=0,0",
                        "--ignore-certificate-errors",
                        "--disable-blink-features=AutomationControlled",
                    ],
                )
                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                    ),
                )
                page = await context.new_page()
                await stealth_async(page)

                logger.info(f"Відкриваємо сторінку {self.base_url}...")
                await page.goto(self.base_url, timeout=60000, wait_until="domcontentloaded")
                await asyncio.sleep(2)

                title = await page.title()
                if "captcha" in title.lower() or "robot" in title.lower():
                    logger.error("Amazon виявив бота (CAPTCHA / Robot Check).")
                    await browser.close()
                    return results

                for _ in range(5):
                    await page.evaluate("window.scrollBy(0, 800)")
                    await asyncio.sleep(0.7)

                cards = await page.query_selector_all(
                    ".p13n-sc-uncoverable-faceout, #gridItemRoot, .zg-grid-general-faceout"
                )
                logger.info(f"Знайдено {len(cards)} карточок товарів на сторінці.")

                for card in cards[:max_items]:
                    try:
                        category = "Best Sellers"
                        try:
                            cat_text = await card.evaluate("""el => {
                                let parent = el.closest('div._cDEzb_card_1L-kr, div.a-carousel-container, div[data-carousel-category]') || el.parentElement;
                                while (parent && parent !== document.body) {
                                    let h2 = parent.querySelector('h2, .a-carousel-heading, ._cDEzb_carousel-heading_8e94y');
                                    if (h2 && h2.innerText.trim()) return h2.innerText.trim();
                                    let prev = parent.previousElementSibling;
                                    while (prev) {
                                        let ph2 = prev.querySelector('h2, .a-carousel-heading') || (prev.tagName === 'H2' ? prev : null);
                                        if (ph2 && ph2.innerText.trim()) return ph2.innerText.trim();
                                        prev = prev.previousElementSibling;
                                    }
                                    parent = parent.parentElement;
                                }
                                return 'Best Sellers';
                            }""")
                            if cat_text:
                                category = (
                                    cat_text.replace("Best Sellers in", "")
                                    .replace("Best Sellers", "")
                                    .strip()
                                    or "Best Sellers"
                                )
                        except Exception:
                            pass

                        t_el = (
                            await card.query_selector("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
                            or await card.query_selector("div._cDEzb_p13n-sc-css-line-clamp-2_EWgCb")
                            or await card.query_selector("div._cDEzb_p13n-sc-css-line-clamp-1_1qL0f")
                            or await card.query_selector("a.a-link-normal span div")
                            or await card.query_selector("a.a-link-normal span")
                        )
                        name = (await t_el.inner_text()).strip() if t_el else None
                        if not name or len(name) < 3:
                            continue

                        p_el = (
                            await card.query_selector("span._cDEzb_p13n-sc-price_3mJ9Z")
                            or await card.query_selector("span.a-price span.a-offscreen")
                            or await card.query_selector("span.p13n-sc-price")
                            or await card.query_selector("span.a-color-price")
                        )
                        price: float = 0.0
                        if p_el:
                            p_text = await p_el.inner_text()
                            match = re.search(r"[\d,]+\.\d{2}", p_text)
                            if match:
                                price = float(match.group().replace(",", ""))

                        r_el = await card.query_selector(
                            "i.a-icon-star-small span.a-icon-alt"
                        ) or await card.query_selector("span.a-icon-alt")
                        rating: float = 0.0
                        if r_el:
                            r_text = await r_el.inner_text()
                            r_match = re.search(r"(\d+(\.\d+)?)", r_text)
                            if r_match:
                                rating = float(r_match.group(1))

                        rev_el = (
                            await card.query_selector("div.a-icon-row + div span.a-size-small")
                            or await card.query_selector("a.a-link-normal span.a-size-small")
                            or await card.query_selector("span.a-size-small")
                        )
                        reviews: int = 0
                        if rev_el:
                            rev_text = await rev_el.inner_text()
                            rev_clean = rev_text.replace(",", "").replace(".", "")
                            rev_match = re.search(r"\d+", rev_clean)
                            if rev_match:
                                reviews = int(rev_match.group())

                        link_el = await card.query_selector(
                            "a.a-link-normal[role='link']"
                        ) or await card.query_selector("a.a-link-normal")
                        product_url: str = ""
                        if link_el:
                            href = await link_el.get_attribute("href")
                            if href:
                                asin_match = re.search(r"/(?:dp|gp/product|product)/([A-Z0-9]{10})", href)
                                if asin_match:
                                    product_url = f"https://www.amazon.com/dp/{asin_match.group(1)}"
                                else:
                                    clean_href = re.sub(r"/ref=.*", "", href.split("?")[0])
                                    if clean_href.startswith("http"):
                                        product_url = clean_href
                                    else:
                                        product_url = f"https://www.amazon.com{clean_href}"

                        img_el = await card.query_selector("img")
                        image_url: str = (
                            await img_el.get_attribute("src") if img_el else ""
                        )

                        # Prevent in-batch duplicate items
                        if any(r["name"].lower() == name.lower() or (product_url and r["product_url"] == product_url) for r in results):
                            continue

                        results.append(
                            {
                                "name": name,
                                "category": category,
                                "price": price,
                                "rating": rating,
                                "number_of_reviews": reviews,
                                "product_url": product_url or "https://www.amazon.com",
                                "image_url": image_url or "https://via.placeholder.com/150",
                            }
                        )
                    except Exception as item_err:
                        logger.warning(f"Помилка при обробці товару: {item_err}")
                        continue

                await browser.close()
        except Exception as e:
            logger.error(f"Помилка під час скрапінгу Amazon: {e}")

        logger.info(f"Успішно зібрано {len(results)} реальних товарів з Amazon.")
        return results
