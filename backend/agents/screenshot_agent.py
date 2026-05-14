from models.schemas import MarketingInsights, ScreenshotSelection


def select_screenshots(
    screenshots: list[str],
    marketing_insights: MarketingInsights,
) -> ScreenshotSelection:
    if not screenshots:
        return ScreenshotSelection(
            hero_screenshot=None,
            gallery_screenshots=[],
            selection_reason="No screenshots were available from the Google Play listing.",
        )

    # MVP heuristic:
    # Google Play usually orders screenshots intentionally.
    # We use the first screenshot as hero and keep the first 5 for the gallery.
    hero_screenshot = screenshots[0]
    gallery_screenshots = screenshots[:5]

    return ScreenshotSelection(
        hero_screenshot=hero_screenshot,
        gallery_screenshots=gallery_screenshots,
        selection_reason=(
            "Selected the first Google Play screenshot as the hero image because "
            "store listings usually place the most representative marketing visual first. "
            f"The gallery was limited to the strongest first {len(gallery_screenshots)} screenshots "
            "to keep the landing page focused and mobile-friendly."
        ),
    )