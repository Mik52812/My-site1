import os
import re
import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime, timezone

# Science RSS Sources
SOURCES = {
    "NASA News": "https://www.nasa.gov/news-release/feed/",
    "SpaceNews": "https://spacenews.com/feed/",
    "Universe Today": "https://www.universetoday.com/feed/",
    "ESA Top News": "https://www.esa.int/rssfeed/Our_Activities/Space_News",
    "Phys.org Archaeology": "https://phys.org/rss-feed/archaeology-news/"
}

# Target Keywords (case-insensitive search)
KEYWORDS = ["astronomy", "exoplanet", "uap", "ufo", "archeology", "archaeology", "discovery", "hypothesis"]

def clean_html(text):
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    cleaner = re.compile('<.*?>')
    return re.sub(cleaner, '', text).strip()

def fetch_and_filter():
    report = []
    total_found = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for name, url in SOURCES.items():
        report.append(f"=== {name} ===")
        found_in_source = 0
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()

            root = ET.fromstring(xml_data)
            items = root.findall('.//item')

            for item in items:
                title = item.findtext('title', default='').strip()
                link = item.findtext('link', default='').strip()
                description = clean_html(item.findtext('description', default=''))

                # Search keywords in title + description
                combined_text = f"{title} {description}".lower()
                matched_keywords = [kw for kw in KEYWORDS if kw in combined_text]

                if matched_keywords:
                    found_in_source += 1
                    total_found += 1
                    # Truncate summary to 250 characters
                    short_desc = (description[:250] + '...') if len(description) > 250 else description
                    report.append(
                        f"\n📍 Title: {title}\n"
                        f"🔗 Link: {link}\n"
                        f"🏷️ Tags: {', '.join(matched_keywords)}\n"
                        f"📝 Preview: {short_desc}\n"
                        f"{'-'*40}"
                    )

            if found_in_source == 0:
                report.append("No news matched your target keywords today.\n")

        except Exception as e:
            report.append(f"Error fetching source {name}: {e}\n")
        
        report.append("\n")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = f"📊 Science News Report — {timestamp} ({total_found} items found)\n" + "="*60 + "\n\n"
    final_text = header + "\n".join(report)

    with open("news_report.txt", "w", encoding="utf-8") as f:
        f.write(final_text)

if __name__ == "__main__":
    fetch_and_filter()
  
