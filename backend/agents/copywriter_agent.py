from services.llm_service import get_claude
from models.schemas import LandingPageContent


def generate_landing_page_content(
    app_data: dict,
    marketing_insights: dict,
    cta_mode: str,
    selected_screenshots: list[str] | None = None,
) -> LandingPageContent:
    llm = get_claude()

    structured_llm = llm.with_structured_output(LandingPageContent)

    screenshots_for_page = selected_screenshots or app_data.get("screenshots", [])

    prompt = f"""
    You are a senior conversion copywriter and mobile app landing page strategist.

    Your task is to generate structured landing page content for a mobile app.

    The page must include:
    1. Hero section
    2. Features section
    3. Benefits section
    4. Social proof section
    5. Media gallery
    6. FAQ section
    7. SEO metadata

    Conversion copywriting rules:
    - The hero headline should focus on the strongest user outcome.
    - The subheadline should explain the app clearly in one sentence.
    - Features should describe what the app does.
    - Benefits should describe why the user should care.
    - FAQ should reduce objections before conversion.
    - Avoid generic words like "amazing", "revolutionary", or "best" unless supported by the data.
    - Prefer simple, direct language over hype.

    Important rules:
    - Do not invent app capabilities.
    - Base the content only on the provided app data and marketing insights.
    - Make the copy clear, benefit-driven, and conversion-focused.
    - Keep the tone aligned with the recommended landing page tone.
    - Use real selected reviews only for social proof.
    - If no good reviews exist, return an empty social_proof array.
    - Use only the provided selected screenshots for media_gallery.
    - Keep the media_gallery order exactly as provided.
    - Do not generate HTML.
        - Return only structured content matching the schema.

    CTA mode:
    {cta_mode}

    CTA writing rules:
    - If cta_mode is "install", use install-focused CTA text such as "Install Now", "Get the App", or "Download on Google Play".
    - If cta_mode is "stripe_subscription", use subscription-focused CTA text such as "Start Premium", "Start Your Plan", or "Unlock Premium Access".
    - Do not create the CTA URL here. That belongs to the CTA Agent in the next step.

    App data:
    {app_data}

    Marketing insights:
    {marketing_insights}

    Selected screenshots:
    {screenshots_for_page}

    """
    return structured_llm.invoke(prompt)