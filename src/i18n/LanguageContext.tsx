"use client";

import React, { createContext, useContext, useState, useCallback, ReactNode } from "react";
import { Locale } from "@/data/types";

const STORAGE_KEY = "anti-fomo-locale";
const VALID_LOCALES: Locale[] = ["zh", "en", "de"];

interface LanguageContextType {
    locale: Locale;
    setLocale: (locale: Locale) => void;
}

const LanguageContext = createContext<LanguageContextType>({
    locale: "en",
    setLocale: () => { },
});

function getInitialLocale(): Locale {
    if (typeof window === "undefined") return "en";
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored && VALID_LOCALES.includes(stored as Locale)) return stored as Locale;
    return "en";
}

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [locale, setLocaleState] = useState<Locale>(getInitialLocale);

    const setLocale = useCallback((l: Locale) => {
        setLocaleState(l);
        localStorage.setItem(STORAGE_KEY, l);
    }, []);

    return (
        <LanguageContext.Provider value={{ locale, setLocale }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    return useContext(LanguageContext);
}
