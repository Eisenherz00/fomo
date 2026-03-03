"use client";

import { useEffect, useState } from "react";
import { Clock } from "lucide-react";
import { useLanguage } from "@/i18n/LanguageContext";
import { getTranslations } from "@/i18n/translations";

function getNextRefresh(): Date {
    const now = new Date();
    const today6 = new Date(now);
    today6.setHours(6, 0, 0, 0);
    const today18 = new Date(now);
    today18.setHours(18, 0, 0, 0);

    if (now < today6) return today6;
    if (now < today18) return today18;
    // next day 6:00
    const tomorrow6 = new Date(now);
    tomorrow6.setDate(tomorrow6.getDate() + 1);
    tomorrow6.setHours(6, 0, 0, 0);
    return tomorrow6;
}

function formatDiff(ms: number): string {
    if (ms <= 0) return "00:00:00";
    const totalSec = Math.floor(ms / 1000);
    const h = String(Math.floor(totalSec / 3600)).padStart(2, "0");
    const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, "0");
    const s = String(totalSec % 60).padStart(2, "0");
    return `${h}:${m}:${s}`;
}

export default function CountdownTimer() {
    const { locale } = useLanguage();
    const t = getTranslations(locale);

    const [remaining, setRemaining] = useState("");

    useEffect(() => {
        function tick() {
            const diff = getNextRefresh().getTime() - Date.now();
            setRemaining(formatDiff(diff));
        }
        tick();
        const id = setInterval(tick, 1000);
        return () => clearInterval(id);
    }, []);

    return (
        <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 backdrop-blur-sm">
            <Clock className="h-4 w-4 text-cyan-400" />
            <span className="text-xs text-zinc-400">{t.nextRefresh}</span>
            <span className="font-mono text-sm font-bold tracking-widest text-cyan-300">
                {remaining}
            </span>
        </div>
    );
}
