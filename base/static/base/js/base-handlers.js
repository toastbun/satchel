document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded base-handlers.js")

    applyHoverEffectsToListItemNames()
    activateEditButtons()
    activateDeleteButtons()
})

function applyHoverEffectsToListItemNames() {
    const listItems = document.querySelectorAll(".list-item-container")

    for (let listItem of listItems) {
        listItem.addEventListener("mouseover", elementHoverHandler)
        listItem.addEventListener("mouseout", elementHoverHandler)
    }
}

function activateEditButtons() {
    const editButtonContainer = document.querySelector(".item-edit-button-container")

    // if (editButtonContainer) {
    //     editButtonContainer.addEventListener("click", editButtonClickHandler)
    // }
}

function activateDeleteButtons() {
    for (let deleteButton of document.querySelectorAll(".list-item-delete")) {
        deleteButton.addEventListener("click", deleteButtonClickHandler)
    }
}