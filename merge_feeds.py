import feedparser
import hashlib
from datetime import datetime
from feedgen.feed import FeedGenerator

# List of your new feeds
FEED_URLS = [
    "https://www.nato.int/cps/rss/en/natohq/rssFeed.xsl/rssFeed.xml",
    "https://www.defenseone.com/rss/all/",
    "https://www.spacewar.com/spacewar.xml"
]

def main():
    fg = FeedGenerator()
    fg.title("Merged Defense / NATO / SpaceWar Feed")
    fg.link(href="https://yourusername.github.io/your-repo/merged-defense.xml", rel="self")
    fg.description("Aggregated RSS feed from NATO, DefenseOne, and SpaceWar")
    fg.language("en")

    seen = set()
    all_entries = []

    for url in FEED_URLS:
        print(f"Fetching {url}")
        try:
            feed = feedparser.parse(url)
            print(f" → {len(feed.entries)} entries")
            for entry in feed.entries:
                link = entry.get("link", "")
                if not link:
                    continue
                uid = hashlib.md5(link.encode("utf-8")).hexdigest()
                if uid not in seen:
                    seen.add(uid)
                    all_entries.append(entry)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Sort entries by published or updated time, newest first
    def get_date(entry):
        return entry.get("published_parsed") or entry.get("updated_parsed") or datetime.utcnow().timetuple()

    all_entries.sort(key=get_date, reverse=True)

    # Optionally limit to the most recent X items
    all_entries = all_entries[:100]

    for entry in all_entries:
        fe = fg.add_entry()
        fe.title(entry.get("title", "No title"))
        fe.link(href=entry.get("link", ""))
        fe.description(entry.get("summary", "") or entry.get("description", ""))
        if "published" in entry:
            fe.pubDate(entry.published)

    fg.rss_file("merged-defense.xml")
    print("Wrote merged-defense.xml")

if __name__ == "__main__":
    main()
