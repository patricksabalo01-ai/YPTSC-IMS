/* ==================================================
   YPTSC IMS
   THEME CONTROLLER
   ENTERPRISE DARK / LIGHT MODE
================================================== */
document.addEventListener(
    "DOMContentLoaded",
    function () {
        initializeTheme();
    }
);
/* ==================================================
   INITIALIZE THEME
================================================== */
function initializeTheme() {
    const themeToggle =
        document.getElementById(
            "themeToggle"
        );
    const themeIcon =
        document.getElementById(
            "themeIcon"
        );
    if (!themeToggle) {
        console.warn(
            "Theme toggle button not found."
        );
        return;
    }
    let savedTheme =
        localStorage.getItem(
            "YPTSC_THEME"
        );
    if (!savedTheme) {
        savedTheme = "dark";
    }
    applyTheme(
        savedTheme,
        themeIcon
    );
    themeToggle.addEventListener(
        "click",
        function () {
            const currentTheme =
                document.documentElement
                    .getAttribute(
                        "data-theme"
                    );
            let newTheme;
            if (currentTheme === "light") {
                newTheme = "dark";
            }
            else {
                newTheme = "light";
            }
            applyTheme(
                newTheme,
                themeIcon
            );
            localStorage.setItem(
                "YPTSC_THEME",
                newTheme
            );
        }
    );
}
/* ==================================================
   APPLY THEME
================================================== */
function applyTheme(
    theme,
    icon
) {
    if (theme === "light") {
        document.documentElement
            .setAttribute(
                "data-theme",
                "light"
            );
        if (icon) {
            icon.className =
                "fa-solid fa-moon";
        }
    }
    else {
        document.documentElement
            .removeAttribute(
                "data-theme"
            );
        if (icon) {
            icon.className =
                "fa-solid fa-sun";
        }
    }
}