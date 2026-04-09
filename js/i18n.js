/**
 * DocConnect Internationalization (i18n) Handler
 */

document.addEventListener('DOMContentLoaded', () => {
    const languageSelector = document.getElementById('languageSelector');
    const currentLang = localStorage.getItem('docconnect_lang') || 'en';
    
    // Set initial language
    if (languageSelector) {
        languageSelector.value = currentLang;
    }
    
    applyTranslations(currentLang);

    // Event listener for language change
    if (languageSelector) {
        languageSelector.addEventListener('change', (e) => {
            const newLang = e.target.value;
            localStorage.setItem('docconnect_lang', newLang);
            applyTranslations(newLang);
        });
    }
});

function applyTranslations(lang) {
    if (!window.translations || !window.translations[lang]) return;
    const langData = window.translations[lang];

    // Find all elements with data-i18n attribute
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (langData[key]) {
            // Check if it's an input placeholder
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = langData[key];
            } else if (el.querySelector('i')) {
                // Preserve icons if they exist
                const icon = el.querySelector('i').outerHTML;
                el.innerHTML = icon + ' ' + langData[key];
            } else {
                el.innerHTML = langData[key];
            }
        }
    });

    // Update document title based on page context if available
    const pageKey = 'page_title_' + window.location.pathname.split('/').pop().replace('.html', '');
    if (langData[pageKey]) {
        document.title = langData[pageKey] + ' - DocConnect';
    }

    // Set HTML lang attribute
    document.documentElement.lang = lang;
}
