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

    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfTokenFromPage()
        }
    })

    location.reload(true)
}

window.addEventListener("load", (event) => {
    console.log("Page is fully loaded.");
})

const theme = document.querySelector("[data-theme]").dataset.theme


/** hover effects **/

const HOVER_COLOR = theme == "light" ? "hsl(0, 0%, 96%)" : "hsl(0, 0%, 21%)"

function toggleElementBackgroundOnHover(element, isHovering, defaultBackgroundColor = "") {
    element.style.backgroundColor = isHovering ? HOVER_COLOR : defaultBackgroundColor
}

function elementHoverHandler(event) {
    if (!["mouseover", "mouseout"].includes(event.type)) {
        return
    }

    toggleElementBackgroundOnHover(event.target.closest(".list-item-container"), event.type == "mouseover")
}