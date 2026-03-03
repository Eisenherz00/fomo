"use client";

import { useLanguage } from "@/i18n/LanguageContext";
import { getTranslations } from "@/i18n/translations";
import { NewsItem } from "@/data/types";
import NewsCard from "./NewsCard";
import { Brain, Globe2, TrendingUp, LucideIcon } from "lucide-react";

type Category = "ai" | "politics" | "stocks";

const meta: Record<Category, { icon: LucideIcon; titleKey: keyof ReturnType<typeof getTranslations>; gradient: string }> = {
    ai: {
        icon: Brain,
        titleKey: "sectionAI",
        gradient: "from-violet-500 to-indigo-500",
    },
    politics: {
        icon: Globe2,
        titleKey: "sectionPolitics",
        gradient: "from-emerald-500 to-teal-500",
    },
    stocks: {
        icon: TrendingUp,
        titleKey: "sectionStocks",
        gradient: "from-amber-500 to-orange-500",
    },
};

export default function NewsSection({
    category,
    items,
}: {
    category: Category;
    items: NewsItem[];
}) {
    const { locale } = useLanguage();
    const t = getTranslations(locale);
    const { icon: Icon, titleKey, gradient } = meta[category];

    return (
        <section>
            {/* Section header */}
            <div className="mb-5 flex items-center gap-3">
                <div
                    className={`flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br ${gradient} shadow-lg`}
                >
                    <Icon className="h-5 w-5 text-white" />
                </div>
                <h2 className="text-lg font-bold tracking-tight text-zinc-100">
                    {t[titleKey]}
                </h2>
            </div>

            {/* Cards */}
            <div className="flex flex-col gap-4">
                {items.map((item) => (
                    <NewsCard key={item.id} item={item} />
                ))}
            </div>
        </section>
    );
}
