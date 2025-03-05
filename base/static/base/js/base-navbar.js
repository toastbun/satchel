document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded base-navbar.js")

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll(".navbar-burger"), 0)

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
        el.addEventListener("click", () => {
            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target)

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle("is-active")
            $target.classList.toggle("is-active")
        })
    })

    const navbarToggleButton = document.querySelector(".navbar-toggle-button")

    navbarToggleButton.addEventListener("click", toggleNavbarHandler)

    document.querySelector(".no-click").addEventListener("click", () => {
        document.querySelector(".navbar-toggle-button").click()
    })
})


async function toggleNavbarHandler(event) {
    const navbarIsActive = document.querySelector(".navbar-toggle-button").classList.contains("is-active")
    const noClickDiv = document.querySelector(".no-click")

    const url = "/toggle_navbar"

    if (noClickDiv.classList.contains("is-active")) {
        noClickDiv.classList.remove("is-active")
    } else {
        noClickDiv.classList.add("is-active")
    }

    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfTokenFromPage()
        },
        body: JSON.stringify({
            active: navbarIsActive
        })
    })
}