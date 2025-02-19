document.addEventListener("DOMContentLoaded", (event) => {
    applyHoverEffectsToListItemNames()
})


function applyHoverEffectsToListItemNames() {
    const listItems = document.querySelectorAll(".list-item-container")

    for (let listItem of listItems) {
        listItem.addEventListener("mouseover", elementHoverHandler)
        listItem.addEventListener("mouseout", elementHoverHandler)
    }
}