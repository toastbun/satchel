document.addEventListener("DOMContentLoaded", (event) => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0)

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {

            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target)

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active')
            $target.classList.toggle('is-active')
        })
    })

    /**
     * 
     * add modal functionality
     * 
     */
    function openModal(modal) {
        modal.classList.add("is-active")
    }

    function closeModal(modal) {
        modal.classList.remove("is-active")
    }

    function closeAllModals() {
        for (let modal of (document.querySelectorAll(".modal") || [])) {
            closeModal(modal)
        }
    }

    for (let trigger of (document.querySelectorAll(".js-modal-trigger") || [])) {
        const modal = trigger.dataset.target
        const target = document.getElementById(modal)

        trigger.addEventListener("click", () => {
            openModal(target)
        })
    }

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