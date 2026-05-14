from google_play_scraper import app, reviews


def extract_app_data(app_url: str):
    app_id = app_url.split("id=")[-1]

    app_data = app(
        app_id,
        lang="en",
        country="us"
    )

    review_data, _ = reviews(
        app_id,
        lang="en",
        country="us",
        count=20
    )

    return {
        "title": app_data.get("title"),
        "description": app_data.get("description"),
        "summary": app_data.get("summary"),
        "score": app_data.get("score"),
        "ratings": app_data.get("ratings"),
        "installs": app_data.get("installs"),
        "icon": app_data.get("icon"),
        "screenshots": app_data.get("screenshots"),
        "reviews": [
            {
                "score": r["score"],
                "content": r["content"]
            }
            for r in review_data
        ]
    }