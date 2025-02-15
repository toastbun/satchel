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
})

window.addEventListener("load", (event) => {
    console.log("Page is fully loaded.");
});