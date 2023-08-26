// Animation triggered when cards of type post are hovered

const items = document.querySelectorAll(".posts__main--secondary");

// play normal
items.forEach((item) => {
    const link = item.querySelector(".posts__main-link--secondary");
    link.addEventListener("mouseover", () => {
        item.classList.remove("out")
        item.classList.add("in");

    });
});

// play in reverse
items.forEach((item) => {
    const link = item.querySelector(".posts__main-link--secondary");
    link.addEventListener("mouseout", () => {
        item.classList.remove("in");
        item.classList.add("out");
    });
});


