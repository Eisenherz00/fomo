import { Locale } from "@/data/types";

// ─── Static UI labels ───────────────────────────────────────────────
export interface Translations {
    siteTitle: string;
    siteSubtitle: string;
    sectionAI: string;
    sectionPolitics: string;
    sectionStocks: string;
    nextRefresh: string;
    source: string;
    footer: string;
    readingTime: string;
}

const translations: Record<Locale, Translations> = {
    zh: {
        siteTitle: "Anti-FOMO Daily",
        siteSubtitle: "每日精华情报 · 只看这一页就够了",
        sectionAI: "前沿科学 / AI",
        sectionPolitics: "全球政治",
        sectionStocks: "股票市场",
        nextRefresh: "距下次刷新",
        source: "来源",
        footer: "© 2026 Anti-FOMO Daily — 你的每日 10 分钟情报站",
        readingTime: "阅读时间 ≈ 10 分钟",
    },
    en: {
        siteTitle: "Anti-FOMO Daily",
        siteSubtitle: "Daily Intel Briefing · One Page Is All You Need",
        sectionAI: "Frontier Science / AI",
        sectionPolitics: "Global Politics",
        sectionStocks: "Stock Market",
        nextRefresh: "Next Refresh In",
        source: "Source",
        footer: "© 2026 Anti-FOMO Daily — Your 10-Minute Daily Intel",
        readingTime: "Reading time ≈ 10 min",
    },
    de: {
        siteTitle: "Anti-FOMO Daily",
        siteSubtitle: "Tägliches Intel-Briefing · Eine Seite genügt",
        sectionAI: "Spitzenforschung / KI",
        sectionPolitics: "Weltpolitik",
        sectionStocks: "Aktienmarkt",
        nextRefresh: "Nächste Aktualisierung in",
        source: "Quelle",
        footer: "© 2026 Anti-FOMO Daily — Dein 10-Minuten-Briefing",
        readingTime: "Lesezeit ≈ 10 Min.",
    },
};

export function getTranslations(locale: Locale): Translations {
    return translations[locale];
}
