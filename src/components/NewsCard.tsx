"use client";

import { useLanguage } from "@/i18n/LanguageContext";
import { getTranslations } from "@/i18n/translations";
import { NewsItem } from "@/data/types";
import { Calendar, ExternalLink } from "lucide-react";

export default function NewsCard({ item }: { item: NewsItem }) {
    const { locale } = useLanguage();
    const t = getTranslations(locale);

    return (
        <article className="group relative rounded-xl border border-white/[0.06] bg-white/[0.03] p-5 transition-all duration-300 hover:border-white/[0.12] hover:bg-white/[0.06] hover:shadow-lg hover:shadow-indigo-500/5">
            {/* Gradient accent line */}
            <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

            <h3 className="mb-2 text-[15px] font-semibold leading-snug text-zinc-100">
                {item.title[locale]}
            </h3>

            <p className="mb-4 text-sm leading-relaxed text-zinc-400">
                {item.summary[locale]}
            </p>

            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 text-xs text-zinc-500">
                    <span className="flex items-center gap-1">
                        <ExternalLink className="h-3 w-3" />
                        {item.source}
                    </span>
                    <span className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {item.date}
                    </span>
                </div>

                {item.url && (
                    <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label={`${t.source}: ${item.source}`}
                        className="flex items-center gap-1 rounded-md border border-indigo-500/30 bg-indigo-500/10 px-2.5 py-1 text-xs font-medium text-indigo-300 transition-all duration-200 hover:border-indigo-400/50 hover:bg-indigo-500/20 hover:text-indigo-200"
                    >
                        <ExternalLink className="h-3 w-3" />
                        {t.source}
                    </a>
                )}
            </div>
        </article>
    );
}
