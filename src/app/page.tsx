"use client";

import { useState, useEffect } from "react";
import { useLanguage } from "@/i18n/LanguageContext";
import { getTranslations } from "@/i18n/translations";
import { DailyData } from "@/data/types";
import { loadNews } from "@/data/loadNews";
import LanguageSwitcher from "@/components/LanguageSwitcher";
import CountdownTimer from "@/components/CountdownTimer";
import NewsSection from "@/components/NewsSection";
import { Shield, Loader2, AlertTriangle } from "lucide-react";

export default function Home() {
  const { locale } = useLanguage();
  const t = getTranslations(locale);

  const [data, setData] = useState<DailyData | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    loadNews()
      .then(setData)
      .catch(() => setError(true));
  }, []);

  if (error) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-3 text-zinc-400">
        <AlertTriangle className="h-8 w-8 text-amber-400" />
        <p className="text-sm">{t.errorLoading}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-400" />
      </div>
    );
  }

  return (
    <div className="mx-auto min-h-screen max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      {/* ── Header ─────────────────────────────────────────────── */}
      <header className="mb-10 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Logo & title */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 shadow-lg shadow-indigo-500/25">
            <Shield className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight text-white">
              {t.siteTitle}
            </h1>
            <p className="text-xs text-zinc-500">{t.siteSubtitle}</p>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-3">
          <span className="hidden rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-[11px] text-zinc-500 sm:inline-block">
            {t.readingTime}
          </span>
          <CountdownTimer />
          <LanguageSwitcher />
        </div>
      </header>

      {/* ── 3-column news grid ─────────────────────────────────── */}
      <main className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        <NewsSection category="ai" items={data.aiNews} />
        <NewsSection category="politics" items={data.politicsNews} />
        <NewsSection category="stocks" items={data.stockNews} />
      </main>

      {/* ── Footer ─────────────────────────────────────────────── */}
      <footer className="mt-16 border-t border-white/[0.06] pt-6 text-center text-xs text-zinc-600">
        <p>{t.footer}</p>
        {data.generatedAt && (
          <p className="mt-1 text-zinc-700">
            {t.lastUpdated}: {new Date(data.generatedAt).toLocaleString(locale === "zh" ? "zh-CN" : locale === "de" ? "de-DE" : "en-US")}
          </p>
        )}
      </footer>
    </div>
  );
}
