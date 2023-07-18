window.onload = function () {
    //cookies
    const cookieBox = document.querySelector(".cookie-box");
    const cookieBtn = document.querySelector(".cookie-btn");

    const showCookie = () => {
        const cookieSeen = localStorage.getItem("cookie");

        if (!cookieSeen) {
            cookieBox.classList.remove("hide");
        }
    };

    const handleCookieBox = () => {
        localStorage.setItem("cookie", "true");
        cookieBox.classList.add("hide");
    };

    cookieBtn.addEventListener("click", handleCookieBox);
    showCookie();

    // navbar

    const navMobile = document.querySelector(".nav__list");
    const navBtn = document.querySelector(".hamburger");
    const navTxt = document.querySelector(".hamburger-text");
    const allNavItems = document.querySelectorAll(".menu-close");

    const showDropdown = function (event) {
        const targ = event.target;

        const drp = document.getElementsByClassName("nav__dropdown");
        for (let i = 0; i < drp.length; i++) {
            if (
                drp[i].previousElementSibling === targ ||
                drp[i].previousElementSibling.children[0] === targ
            ) {
                drp[i].classList.toggle("show");
            } else {
                drp[i].classList.remove("show");
            }
        }
    };

    window.addEventListener("click", showDropdown);

    if (!navBtn.classList.contains("is-active")) {
        // window.addEventListener("mouseover", console.log("hmm5"));
    }

    const closeNav = () => {
        navBtn.classList.remove("is-active");
        navMobile.classList.remove("nav__list--active");
    };

    allNavItems.forEach((item) => {
        item.addEventListener("click", closeNav);
    });

    const handleNav = () => {
        navBtn.classList.toggle("is-active");
        navMobile.classList.toggle("nav__list--active");
        if (navBtn.classList.contains("is-active")) {
            navTxt.textContent = "Zamknij";
            document.body.style.overflow = "hidden";
        } else {
            navTxt.textContent = "Menu";
            document.body.style.overflow = "scroll";
        }
    };

    navBtn.addEventListener("click", handleNav);

    // categories
    const catLinks = document.querySelectorAll(".posts__categories-link");

    const addActiveClass = (event) => {
        event.target.classList.add("posts__categories-link--active");
    };

    catLinks.forEach((btn) => {
        btn.addEventListener("click", addActiveClass);
    });
};