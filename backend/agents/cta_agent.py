import os
from models.schemas import CTAConfigInput, CTAConfig


def generate_cta_config(input_data: CTAConfigInput) -> CTAConfig:
    if input_data.cta_mode == "install":
        return CTAConfig(
            mode="install",
            text=input_data.custom_cta_button_text or "Download on Google Play",
            url=input_data.google_play_url,
            message="Install the app and start using it today.",
            plan_id=None,
        )

    if input_data.cta_mode == "stripe_subscription":
        stripe_url = input_data.stripe_checkout_url or os.getenv("STRIPE_CHECKOUT_URL")

        if not stripe_url:
            raise ValueError(
                "STRIPE_CHECKOUT_URL is required when cta_mode is stripe_subscription"
            )

        return CTAConfig(
            mode="stripe_subscription",
            text=input_data.custom_cta_button_text or "Start Premium",
            url=stripe_url,
            message="Subscribe now to unlock premium access before continuing to the app.",
            plan_id=input_data.plan_id or "pro_monthly",
        )

    raise ValueError("Unsupported CTA mode")