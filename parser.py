import feedparser
from datetime import datetime

# Список RSS-источников с исправленной и стабильной ссылкой на ESA
RSS_SOURCES = {
    "NASA News": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "Space News": "https://spacenews.com/feed/",
    "Universe Today": "https://www.universetoday.com/feed/",
    "ESA Top News": "https://www.esa.int/rssfeed/TopNews",
    "Phys.org Archaeology": "https://phys.org/rss-feed/science-news/archaeology-fossils/"
}

# Ключевые слова для фильтрации новостей
KEYWORDS = [
    "astronomy", "space", "uap", "archaeology", "exoplanet", 
    "mars", "nasa", "esa", "telescope", "asteroid", "comet"
]

def parse_news():
    report_lines = []
    report_lines.append(f"=== DAILY SCIENCE NEWS REPORT ===")
    report_lines.append(f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")

    for source_name, url in RSS_SOURCES.items():
        report_lines.append(f"=== {source_name} ===")
        try:
            feed = feedparser.parse(url)
            
            # Проверяем, удалось ли загрузить ленту и есть ли в ней записи
            if not feed.entries:
                report_lines.append(f"No entries found or failed to parse feed.\n")
                continue

            count = 0
            # Обрабатываем топ-10 записей из ленты
            for entry in feed.entries[:10]:
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                link = entry.get('link', '')

                # Проверяем на наличие ключевых слов (регистронезависимо)
                text_to_check = (title + " " + summary).lower()
                if any(kw in text_to_check for kw in KEYWORDS):
                    report_lines.append(f"- {title}")
                    report_lines.append(f"  Link: {link}\n")
                    count += 1

            if count == 0:
                report_lines.append("No matching news found for today based on keywords.\n")

        except Exception as e:
            report_lines.append(f"Error fetching source {source_name}: {str(e)}\n")

    # Сохраняем результат в файл news_report.txt
    with open("news_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("News report successfully generated and saved to news_report.txt")

if __name__ == "__main__":
    parse_news()
