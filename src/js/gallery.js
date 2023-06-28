function waitForElm(selector) {
    return new Promise((resolve) => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver((mutations) => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
        });
    });
}

waitForElm(".fslightbox-toolbar").then((elm) => {
    console.log("Element is ready");
    const allImgs = document.querySelectorAll(
        ".fslightbox-absoluted",
        ".fslightbox-full-dimension",
        ".fslightbox-flex-centered"
    );
    const newDiv = document.createElement("div");

    const newContent = document.createTextNode("Hi");
    newDiv.appendChild(newContent);
    newDiv.classList.add(
        "fslightbox-toolbar-button",
        "fslightbox-flex-centered"
    );
    elm.appendChild(newDiv);

    newDiv.addEventListener("click", function () {
        for (let i = 0; i < allImgs.length; i++) {
            if (!allImgs[i].style.transform) {
                console.log(allImgs[i]);
                const obj = allImgs[i].firstChild.getElementsByClassName(
                    "fslightbox-source"
                );
                if (obj.length>0) {
                    console.log(allImgs[i+1].firstChild.getElementsByClassName(
                    "fslightbox-source"
                    )[0].src);
                    return;
                }
            }
        }
    });
});


