(function () {
    const body = document.body;
    const toggle = document.querySelector(".sidebarCollapse");

    if (!toggle) return;

    let locked = false;

    // hamburger click → menüyü kilitle
    toggle.addEventListener("click", function (e) {
        if (window.innerWidth > 991) return;

        e.preventDefault();

        body.classList.add("alt-menu");
        locked = true;
    });

    // tema alt-menu'yu silmeye çalışırsa → geri ekle
    new MutationObserver(() => {
        if (
            locked &&
            window.innerWidth <= 991 &&
            !body.classList.contains("alt-menu")
        ) {
            body.classList.add("alt-menu");
        }
    }).observe(body, { attributes: true, attributeFilter: ["class"] });

    // ekran büyürse kilidi kaldır
    window.addEventListener("resize", () => {
        if (window.innerWidth > 991) {
            locked = false;
            body.classList.remove("alt-menu");
        }
    });
})();
