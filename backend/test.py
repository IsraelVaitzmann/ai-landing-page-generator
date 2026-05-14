from services.playstore_service import extract_app_data
from agents.marketing_agent import analyze_marketing
from agents.copywriter_agent import generate_landing_page_content
from agents.cta_agent import generate_cta_config
from models.schemas import CTAConfigInput
from services.file_service import save_json


def main():
    url = "https://play.google.com/store/apps/details?id=com.spotify.music"
    cta_mode = "stripe_subscription"
    app_data = extract_app_data(url)
    marketing_insights = analyze_marketing(app_data)

    landing_page = generate_landing_page_content(
        app_data=app_data,
        marketing_insights=marketing_insights.model_dump(),
        cta_mode=cta_mode
    )

    cta = generate_cta_config(
    CTAConfigInput(
        cta_mode=cta_mode,
        google_play_url=url,
        stripe_checkout_url="https://checkout.stripe.com/demo-checkout-url",
        custom_cta_button_text="Start Premium",
        plan_id="pro_monthly"
    )
)

    output = {
        "app_name": app_data["title"],
        "app_icon": app_data.get("icon"),
        "google_play_url": url,
        "landing_page": landing_page.model_dump(),
        "cta": cta.model_dump()
    }

    path = save_json(output, "final_landing_page_install")

    print(f"Saved output to: {path}")
    print(cta.model_dump_json(indent=2))


if __name__ == "__main__":
    main()