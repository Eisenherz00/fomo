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
    errorLoading: string;
    lastUpdated: string;
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
        errorLoading: "数据加载失败，请稍后重试",
        lastUpdated: "数据更新于",
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
        errorLoading: "Failed to load data. Please try again later.",
        lastUpdated: "Last updated",
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
        errorLoading: "Daten konnten nicht geladen werden. Bitte versuche es später erneut.",
        lastUpdated: "Zuletzt aktualisiert",
    },
};

export function getTranslations(locale: Locale): Translations {
    return translations[locale];
}
