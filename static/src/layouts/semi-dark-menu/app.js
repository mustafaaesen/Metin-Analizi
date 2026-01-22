window.__USER_TOGGLED_SIDEBAR__ = false;
window.__SIDEBAR_BOUND__ = false;

var App = function() {
    var MediaSize = {
        xl: 1200,
        lg: 992,
        md: 991,
        sm: 576
    };
    var Dom = {
        main: document.querySelector('html, body'),
        id: {
            container: document.querySelector("#container"),
        },
        class: {
            navbar: document.querySelector(".navbar"),
            overlay: document.querySelector('.overlay'),
            search: document.querySelector('.toggle-search'),
            searchOverlay: document.querySelector('.search-overlay'),
            searchForm: document.querySelector('.search-form-control'),
            mainContainer: document.querySelector('.main-container'),
            mainHeader: document.querySelector('.header.navbar')
        }
    }

    var categoryScroll = {
        scrollCat: function() {
            var sidebarWrapper = document.querySelectorAll('.sidebar-wrapper li.active')[0];
            var sidebarWrapperTop = sidebarWrapper.offsetTop - 12;
            setTimeout(() => {
                const scroll = document.querySelector('.menu-categories');
                scroll.scrollTop = sidebarWrapperTop;
            }, 50);
        }
    }

    var toggleFunction = {
        sidebar: function($recentSubmenu) {

            /* 🔥 EN KRİTİK FIX: SADECE 1 KEZ BIND */
            if (window.__SIDEBAR_BOUND__) return;
            window.__SIDEBAR_BOUND__ = true;

            var sidebarCollapseEle = document.querySelectorAll('.sidebarCollapse');

            sidebarCollapseEle.forEach(el => {
                el.addEventListener('click', function (sidebar) {
                    sidebar.preventDefault();

                    window.__USER_TOGGLED_SIDEBAR__ = true;

                    getSidebar = document.querySelector('.sidebar-wrapper');

                    if ($recentSubmenu === true) {
                        if (document.querySelector('.collapse.submenu').classList.contains('show')) {
                            document.querySelector('.submenu.show').classList.add('mini-recent-submenu');
                            getSidebar.querySelector('.collapse.submenu').classList.remove('show');
                            document.querySelector('.collapse.submenu').parentNode
                                .querySelector('.dropdown-toggle')
                                .setAttribute('aria-expanded', 'false');
                        } else {
                            if (Dom.class.mainContainer.classList.contains('sidebar-closed')) {
                                if (document.querySelector('.collapse.submenu').classList.contains('recent-submenu')) {
                                    getSidebar.querySelector('.collapse.submenu.recent-submenu').classList.add('show');
                                    document.querySelector('.collapse.submenu.recent-submenu')
                                        .parentNode.querySelector('.dropdown-toggle')
                                        .setAttribute('aria-expanded', 'true');
                                    document.querySelector('.submenu').classList.remove('mini-recent-submenu');
                                } else {
                                    document.querySelector('li.active .submenu').classList.add('recent-submenu');
                                    getSidebar.querySelector('.collapse.submenu.recent-submenu').classList.add('show');
                                    document.querySelector('.collapse.submenu.recent-submenu')
                                        .parentNode.querySelector('.dropdown-toggle')
                                        .setAttribute('aria-expanded', 'true');
                                    document.querySelector('.submenu').classList.remove('mini-recent-submenu');
                                }
                            }
                        }
                    }

                    Dom.class.mainContainer.classList.toggle("sidebar-closed");
                    Dom.class.mainHeader.classList.toggle('expand-header');
                    Dom.class.mainContainer.classList.toggle("sbar-open");
                    Dom.class.overlay.classList.toggle('show');
                    Dom.main.classList.toggle('sidebar-noneoverflow');
                });
            });
        },

        onToggleSidebarSubmenu: function() {
            ['mouseenter', 'mouseleave'].forEach(function(e){
                document.querySelector('.sidebar-wrapper').addEventListener(e, function() {
                    if (document.querySelector('body').classList.contains('alt-menu')) {
                        if (document.querySelector('.main-container').classList.contains('sidebar-closed')) {
                            if (e === 'mouseenter') {
                                document.querySelector('li.menu .submenu').classList.remove('show');
                                document.querySelector('li.menu.active .submenu').classList.add('recent-submenu');
                                document.querySelector('li.menu.active')
                                    .querySelector('.collapse.submenu.recent-submenu')
                                    .classList.add('show');
                            } else {
                                document.querySelectorAll('li.menu').forEach(element => {
                                    var submenuShowEle = element.querySelector('.collapse.submenu.show');
                                    if (submenuShowEle) submenuShowEle.classList.remove('show');
                                });
                            }
                        }
                    }
                });
            });
        },

        offToggleSidebarSubmenu: function () {},

        overlay: function() {
            document.querySelector('#dismiss, .overlay')
                .addEventListener('click', function () {
                    Dom.class.mainContainer.classList.add('sidebar-closed');
                    Dom.class.mainContainer.classList.remove('sbar-open');
                    Dom.class.overlay.classList.remove('show');
                    Dom.main.classList.remove('sidebar-noneoverflow');
                });
        },

        search: function() {
            if (Dom.class.search) {
                Dom.class.search.addEventListener('click', function() {
                    this.classList.add('show-search');
                    Dom.class.searchOverlay.classList.add('show');
                    document.body.classList.add('search-active');
                });

                Dom.class.searchOverlay.addEventListener('click', function() {
                    this.classList.remove('show');
                    Dom.class.search.classList.remove('show-search');
                    document.body.classList.remove('search-active');
                });
            }
        },

        themeToggle: function () {
            var togglethemeEl = document.querySelector('.theme-toggle');
            if (!togglethemeEl) return;

            togglethemeEl.addEventListener('click', function() {
                var getLocalStorage = localStorage.getItem("theme");
                if (!getLocalStorage) return;

                var parseObj = JSON.parse(getLocalStorage);
                parseObj.settings.layout.darkMode = !parseObj.settings.layout.darkMode;
                localStorage.setItem("theme", JSON.stringify(parseObj));

                document.body.classList.toggle('dark', parseObj.settings.layout.darkMode);
            });
        }
    }

    function sidebarFunctionality() {
        function sidebarCloser() {
            if (window.innerWidth <= 991 && window.__USER_TOGGLED_SIDEBAR__ === true) {
                return;
            }

            if (window.innerWidth <= 991 ) {
                Dom.id.container.classList.add("sidebar-closed");
                Dom.class.overlay.classList.remove('show');
            }
        }

        sidebarCloser();
        window.addEventListener('resize', sidebarCloser);
    }

    return {
        init: function() {
            toggleFunction.overlay();
            toggleFunction.search();
            toggleFunction.themeToggle();
            toggleFunction.sidebar();   // 🔥 artık sadece 1 kez bind edilir
            sidebarFunctionality();
        }
    }

}();

window.addEventListener('load', function() {
    App.init();
});

