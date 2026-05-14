from urllib.parse import urlparse, parse_qs
from google_play_scraper import app, reviews


def extract_app_id(app_url: str) -> str:
    parsed = urlparse(app_url)

    if "play.google.com" not in parsed.netloc:
        raise ValueError("Please enter a valid Google Play Store URL.")

    query = parse_qs(parsed.query)
    app_id = query.get("id", [None])[0]

    if not app_id:
        raise ValueError("Google Play URL must include an app id.")

    return app_id


def extract_app_data(app_url: str):
    app_id = extract_app_id(app_url)

    try:
        app_data = app(app_id, lang="en", country="us")

        review_data, _ = reviews(
            app_id,
            lang="en",
            country="us",
            count=20,
        )

    except Exception:
        raise ValueError(
            "Could not find this app on Google Play. Please check the URL and try again."
        )

    return {
        "title": app_data.get("title"),
        "description": app_data.get("description"),
        "summary": app_data.get("summary"),
        "score": app_data.get("score"),
        "ratings": app_data.get("ratings"),
        "installs": app_data.get("installs"),
        "icon": app_data.get("icon"),
        "screenshots": app_data.get("screenshots") or [],
        "reviews": [
            {
                "score": r.get("score"),
                "content": r.get("content"),
            }
            for r in review_data
            if r.get("content")
        ],
    }