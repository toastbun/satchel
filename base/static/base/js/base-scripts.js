document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded base-scripts.js")

    for (let themeToggleButton of document.querySelectorAll(".theme-toggle")) {
        themeToggleButton.addEventListener("click", themeToggleButtonClickHandler)
    }
})

function getCsrfTokenFromPage() {
    try {
        return document.querySelector("[data-token]").dataset.token
    } catch (error) {
        console.log(`getCsrfTokenFromPage | Error: No element was found on the document with a "data-token" attribute.`)

        return null
    }
}

async function themeToggleButtonClickHandler(event) {
    const url = "/switch_theme"

    const page = document.querySelector("html")
    page.dataset["theme"] = page.dataset["theme"] == "dark" ? "light" : "dark"

    for (let themeIconContainer of document.querySelectorAll(".theme-toggle")) {
        const themeIcon = themeIconContainer.querySelector("i")
        themeIcon.classList.remove("fa-sun", "fa-moon")
        themeIcon.classList.add(page.dataset["theme"] == "dark" ? "fa-sun" : "fa-moon")
    }

    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfTokenFromPage()
        }
    })

    // location.reload(true)
}

window.addEventListener("load", (event) => {
    console.log("Page is fully loaded.");
})

const theme = document.querySelector("[data-theme]").dataset.theme


/** hover effects **/

function toggleElementBackgroundOnHover(element, isHovering, defaultBackgroundColor = "") {
    const hoverColor = document.querySelector("[data-theme]").dataset.theme == "dark" ? "hsl(0, 0%, 21%)" : "hsl(0, 0%, 96%)"
    element.style.backgroundColor = isHovering ? hoverColor : defaultBackgroundColor
}

function elementHoverHandler(event) {
    if (!["mouseover", "mouseout"].includes(event.type)) {
        return
    }

    toggleElementBackgroundOnHover(event.target.closest(".list-item-container"), event.type == "mouseover")
}