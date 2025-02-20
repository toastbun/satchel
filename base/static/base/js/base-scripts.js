document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded base-scripts.js")

    for (let themeToggleButton of document.querySelectorAll(".theme-toggle")) {
        themeToggleButton.addEventListener("click", themeToggleButtonClickHandler)
    }
})

async function themeToggleButtonClickHandler(e) {
    const url = "/switch_theme"

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[data-token]").dataset.token
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