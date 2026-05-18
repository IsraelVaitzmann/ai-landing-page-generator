from models.schemas import LandingPageContent, CopyStrategy
from services.llm_service import get_claude

def get_temperature_for_strategy(strategy: CopyStrategy) -> float:
    if strategy == CopyStrategy.conservative:
        return 0.25

    if strategy == CopyStrategy.creative:
        return 0.95

    return 0.65

def get_strategy_rules(strategy: CopyStrategy) -> str:
    if strategy == CopyStrategy.conservative:
        return """
        Strategy: Conservative / Trust-Focused.

        Write like a professional SaaS/product marketing page.

        Requirements:
        - Use clear, direct, practical language.
        - Focus on trust, usefulness, reliability, and ease of use.
        - Avoid hype, slang, humor, exaggeration, or dramatic claims.
        - The hero headline should be simple and benefit-focused.
        - The subheadline should explain exactly what the app helps users do.
        - Features should sound stable, credible, and practical.
        - FAQ answers should reduce risk and uncertainty.
        - CTA language should feel safe and direct.

        Style examples:
        - "Organize your work in one place"
        - "A simpler way to manage your daily tasks"
        - "Built to help you stay focused and consistent"

        Do not use:
        - "transform your life"
        - "unlock your potential"
        - "game-changing"
        - "crush it"
        - overly emotional or dramatic language
        """

    if strategy == CopyStrategy.creative:
        return """
        Strategy: Creative / Emotion-Driven.

        Write like a bold consumer growth landing page.

        Requirements:
        - Use energetic, memorable, emotionally engaging copy.
        - Use stronger hooks and curiosity-driven phrasing.
        - Focus on aspiration, momentum, identity, and emotional payoff.
        - The hero headline should feel punchy and attention-grabbing.
        - The subheadline should make the user feel the benefit quickly.
        - Features should be framed as exciting user outcomes.
        - FAQ answers can be more conversational and persuasive.
        - CTA language should feel more premium and action-oriented.

        Style examples:
        - "Turn everyday chaos into momentum"
        - "Your next habit starts here"
        - "Make progress feel effortless"
        - "Unlock the smarter way to move, create, or grow"

        Do not invent app features.
        Do not make medical, financial, or unrealistic claims.
        Keep the claims grounded in the app data.
        """

    return """
    Strategy: Balanced.

    Write professional, benefit-driven landing page copy.
    Balance clarity, persuasion, and creativity.
    """
def generate_landing_page_content(
    app_data: dict,
    marketing_insights: dict,
    cta_mode: str,
    selected_screenshots: list[str] | None = None,
    strategy: CopyStrategy = CopyStrategy.balanced,
) -> LandingPageContent:
    llm = get_claude(temperature=get_temperature_for_strategy(strategy))

    structured_llm = llm.with_structured_output(LandingPageContent)

    screenshots_for_page = selected_screenshots or app_data.get("screenshots", [])
    strategy_rules = get_strategy_rules(strategy)

    prompt = f"""
    You are a senior conversion copywriter and mobile app landing page strategist.

    Generate structured landing page content for a mobile app.

    {strategy_rules}

    Required sections:
    1. Hero section
    2. Features section
    3. Benefits section
    4. Social proof section
    5. Media gallery
    6. FAQ section
    7. SEO metadata

    Rules:
    - Do not invent app capabilities.
    - Base the content only on the provided app data and marketing insights.
    - Use real selected reviews only for social proof.
    - If no good reviews exist, return an empty social_proof array.
    - Use only the selected screenshots for media_gallery.
    - Keep media_gallery order exactly as provided.
    - Do not generate HTML.
    - Return only structured content matching the schema.

    CTA mode:
    {cta_mode}

    App data:
    {app_data}

    Marketing insights:
    {marketing_insights}

    Selected screenshots:
    {screenshots_for_page}
    """

    return structured_llm.invoke(prompt)