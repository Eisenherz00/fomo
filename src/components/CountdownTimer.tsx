"use client";

import { useEffect, useState } from "react";
import { Clock } from "lucide-react";
import { useLanguage } from "@/i18n/LanguageContext";
import { getTranslations } from "@/i18n/translations";

/**
 * GitHub Actions schedule: 04:30 UTC and 16:30 UTC.
 * Compute the next refresh target in UTC, then convert to local ms diff.
 */
function getNextRefresh(): Date {
    const now = new Date();
    const todayUTC = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));

    // Two refresh points each day (UTC)
    const slot1 = new Date(todayUTC.getTime() + 4 * 3600_000 + 30 * 60_000);  // 04:30 UTC
    const slot2 = new Date(todayUTC.getTime() + 16 * 3600_000 + 30 * 60_000); // 16:30 UTC

    if (now < slot1) return slot1;
    if (now < slot2) return slot2;
    // Next day 04:30 UTC
    return new Date(slot1.getTime() + 86_400_000);
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
