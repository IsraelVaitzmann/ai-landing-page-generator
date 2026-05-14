import Image from "next/image";
import { FinalLandingPagePayload } from "../types/landing-page";

type Props = {
  data: FinalLandingPagePayload;
};

export function LandingPagePreview({ data }: Props) {
  const page = data.landing_page;
  const cta = data.cta;

  return (
    <section className="overflow-hidden rounded-3xl bg-white text-slate-950 shadow-xl">
      <div className="grid gap-8 bg-slate-950 p-8 text-white md:grid-cols-2 md:p-12">
        <div>
          <div className="mb-6 flex items-center gap-3">
            {data.app_icon && (
              <Image
                src={data.app_icon}
                alt={`${data.app_name} icon`}
                width={56}
                height={56}
                className="rounded-2xl"
              />
            )}
            <span className="font-semibold">{data.app_name}</span>
          </div>

          <h1 className="text-4xl font-bold md:text-5xl">
            {page.hero.headline}
          </h1>

          <p className="mt-4 text-lg leading-8 text-slate-300">
            {page.hero.subheadline}
          </p>

          <a
            href={data.cta.url}
            target="_blank"
            rel="noreferrer"
            className="mt-8 inline-block rounded-full bg-white px-6 py-3 font-semibold text-slate-950"
          >
            {data.cta.text}
          </a>

          <p className="mt-3 text-sm text-slate-400">{cta.message}</p>
        </div>

        {page.media_gallery?.[0] && (
          <div className="flex justify-center">
            <Image
              src={page.media_gallery[0]}
              alt="App screenshot"
              width={260}
              height={520}
              className="rounded-3xl shadow-2xl"
            />
          </div>
        )}
      </div>

      <div className="p-8 text-slate-950 md:p-12">
        <h2 className="text-2xl font-bold">Features</h2>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {page.features.map((feature, index) => (
            <div key={index} className="rounded-2xl border bg-slate-50 p-5">
              <h3 className="font-semibold">{feature.title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-slate-50 p-8 text-slate-950 md:p-12">
        <h2 className="text-2xl font-bold">Benefits</h2>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {page.benefits.map((benefit, index) => (
            <div key={index} className="rounded-2xl bg-white p-5 shadow-sm">
              <h3 className="font-semibold">{benefit.title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                {benefit.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {page.social_proof.length > 0 && (
        <div className="p-8 md:p-12">
          <h2 className="text-2xl font-bold">What users say</h2>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {page.social_proof.map((review, index) => (
              <blockquote key={index} className="rounded-2xl border p-5">
                <p className="text-slate-700">“{review.quote}”</p>
                <footer className="mt-3 text-sm text-slate-500">
                  {review.source}
                  {review.rating ? ` · ${review.rating}/5` : ""}
                </footer>
              </blockquote>
            ))}
          </div>
        </div>
      )}

      {page.media_gallery.length > 1 && (
        <div className="bg-slate-50 p-8 md:p-12">
          <h2 className="text-2xl font-bold">Screenshots</h2>

          <div className="mt-6 flex gap-4 overflow-x-auto pb-4">
            {page.media_gallery.slice(1, 6).map((image, index) => (
              <Image
                key={index}
                src={image}
                alt={`Screenshot ${index + 1}`}
                width={180}
                height={360}
                className="rounded-3xl border bg-white shadow-sm"
              />
            ))}
          </div>
        </div>
      )}

      <div className="p-8 md:p-12">
        <h2 className="text-2xl font-bold">FAQ</h2>

        <div className="mt-6 space-y-4">
          {page.faq.map((item, index) => (
            <div key={index} className="rounded-2xl border p-5">
              <h3 className="font-semibold">{item.question}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                {item.answer}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-slate-950 p-8 text-center text-white md:p-12">
        <h2 className="text-3xl font-bold">Ready to get started?</h2>
        <p className="mx-auto mt-3 max-w-2xl text-slate-300">{cta.message}</p>

        <a
          href={cta.url}
          target="_blank"
          rel="noreferrer"
          className="mt-6 inline-block rounded-full bg-white px-6 py-3 font-semibold text-slate-950"
        >
          {cta.text}
        </a>
      </div>
    </section>
  );
}