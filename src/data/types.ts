// ─── Shared type definitions ────────────────────────────────────────
// Used by both the frontend components and the Python data pipeline.

export type Locale = "zh" | "en" | "de";

export interface LocalizedText {
    zh: string;
    en: string;
    de: string;
}

export interface NewsItem {
    id: string;
    title: LocalizedText;
    summary: LocalizedText;
    source: string;
    date: string;
    url?: string;
}

export interface DailyData {
    generatedAt: string;
    aiNews: NewsItem[];
    politicsNews: NewsItem[];
    stockNews: NewsItem[];
}
