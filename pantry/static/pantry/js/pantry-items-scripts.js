document.addEventListener("DOMContentLoaded", (event) => {
    // move the auto-complete dropdown to the input field

    const ingredientNameInput = document.querySelector("#id_ingredient")
    const ingredientNameInputContainer = ingredientNameInput.parentNode.parentNode
    const ingredientNameDropdown = document.querySelector("#ingredient-dropdown")

    ingredientNameDropdown.style.top = "-12px"
    ingredientNameDropdown.style.position = "relative"
    ingredientNameDropdown.style.width = "100%"
    ingredientNameDropdown.querySelector(".dropdown-menu").style.width = "100%"

    ingredientNameInputContainer.after(ingredientNameDropdown)

    for (let textInputFieldWithAutocomplete of document.querySelectorAll(".autocomplete")) {
        textInputFieldWithAutocomplete.addEventListener("input", autocompleteTextInputUpdateHandler)
    }
})