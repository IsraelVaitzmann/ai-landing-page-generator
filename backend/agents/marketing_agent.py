from services.llm_service import get_claude
from models.schemas import MarketingInsights


def analyze_marketing(app_data: dict) -> MarketingInsights:
    llm = get_claude()

    structured_llm = llm.with_structured_output(MarketingInsights)

    prompt = f"""
    You are a senior mobile growth strategist and landing page conversion expert.

    Analyze the following Google Play app data and produce structured marketing insights.

    Your job:
    1. Identify the most likely target audience.
    2. Extract the strongest value proposition.
    3. Pick the most marketable features.
    4. Find emotional hooks that can increase conversions.
    5. Select only reviews that are useful for landing page social proof.
    6. Recommend the tone of the page.
    7. Decide the strongest hero section angle.

    Review selection rules:
    - Prefer reviews with score 4 or 5.
    - Prefer specific reviews over generic reviews.
    - Prefer reviews that mention outcomes, benefits, or emotions.
    - Avoid empty, vague, or very short reviews.
    - Select at least 3 reviews if enough good reviews exist.
    - Preserve the original review wording.
    - Do not summarize reviews.
    - Do not invent reviews.

    App data:
    {app_data}
    """

    return structured_llm.invoke(prompt)