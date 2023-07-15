// Animation triggered when cards of type post are hovered

const items = document.querySelectorAll(".posts__main--secondary");


// play normal
items.forEach((item) => {
    const link = item.querySelector(".posts__main-link--secondary");
    link.addEventListener("mouseover", () => {
        item.classList.remove("out")
        item.classList.add("in");

        console.log(item);
    });
});

// play in reverse
items.forEach((item) => {
    const link = item.querySelector(".posts__main-link--secondary");
    link.addEventListener("mouseout", () => {
        // item.style.opacity = 0; // avoid showing the init style while switching the 'active' class
        item.classList.remove("in");
        item.classList.add("out");
    });

    // force dom update
    // setTimeout(() => {
    //     item.classList.add("in");
    //     // item.style.opacity = "";
    // }, 5);

    // item.addEventListener("animationend", onanimationend);
});

// function onanimationend() {
//     items.forEach((item) => {
//         item.classList.remove("in", "out");
//         item.removeEventListener("animationend", onanimationend);
//     });
// }
