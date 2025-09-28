import { useState } from "react";

export const LanguageSelector = ({ onLanguageChange, selectedLanguage }) => {
  const languages = [
    { code: "georgian", name: "ქართული", flag: "🇬🇪" },
    { code: "english", name: "English", flag: "🇺🇸" }
  ];

  return (
    <div className="flex gap-1 bg-black/20 rounded-lg p-1">
      {languages.map((language) => (
        <button
          key={language.code}
          onClick={() => onLanguageChange(language.code)}
          className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
            selectedLanguage === language.code
              ? 'bg-white text-black'
              : 'text-white hover:bg-white/10'
          }`}
        >
          <span>{language.flag}</span>
          <span>{language.name}</span>
        </button>
      ))}
    </div>
  );
};
