"use client";

import { useLanguage } from "@/i18n/LanguageContext";
import { Locale } from "@/data/types";

const locales: Locale[] = ["zh", "en", "de"];
const labels: Record<Locale, string> = { zh: "中文", en: "EN", de: "DE" };

export default function LanguageSwitcher() {
    const { locale, setLocale } = useLanguage();

    return (
        <div className="flex items-center rounded-full border border-white/10 bg-white/5 p-0.5 backdrop-blur-sm">
            {locales.map((l) => (
                <button
                    key={l}
                    onClick={() => setLocale(l)}
                    className={`rounded-full px-3.5 py-1.5 text-xs font-semibold tracking-wide transition-all duration-200 ${locale === l
                        ? "bg-gradient-to-r from-indigo-500 to-cyan-400 text-white shadow-lg shadow-indigo-500/30"
                        : "text-zinc-400 hover:text-white"
                        }`}
                >
                    {labels[l]}
                </button>
            ))}
        </div>
    );
}
