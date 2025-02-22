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
        textInputFieldWithAutocomplete.addEventListener("keydown", autocompleteTextInputScrollHandler)
    }
})


/**
 * 
 * functions
 * 
 **/

function getCsrfTokenFromForm(formElement) {
    return formElement.closest("form").querySelector("[name='csrfmiddlewaretoken']").value
}


function getAssociatedDropdown(formElement) {
    return formElement.closest("form").querySelector(`#${formElement.name}-dropdown`)
}

async function autocompleteTextInputUpdateHandler(event) {
    const csrfToken = getCsrfTokenFromForm(event.target)
    const ingredientNames = await queryIngredientNames(event.target.value, csrfToken)
    const dropdown = getAssociatedDropdown(event.target)

    if (!(dropdown.classList.contains("is-active"))) {
        dropdown.classList.add("is-active")
    } else {
        if (event.target.value == "") {
            dropdown.classList.remove("is-active")
        }
    }

    const dropdownContent = dropdown.querySelector(".dropdown-content")

    dropdownContent.replaceChildren()

    if (ingredientNames.data.length) {
        for (let ingredientName of ingredientNames.data) {
            const newSelectElement = document.createElement("div")
            const newSelectElementText = document.createTextNode(ingredientName)
    
            newSelectElement.classList.add("dropdown-item", "unselectable")
            newSelectElement.appendChild(newSelectElementText)

            dropdownContent.appendChild(newSelectElement)
        }
    } else {
        dropdown.classList.remove("is-active")
    }

    for (let dropdownItem of document.querySelectorAll(".dropdown-item")) {
        dropdownItem.addEventListener("mouseover", elementHoverHandler)
        dropdownItem.addEventListener("mouseout", elementHoverHandler)

        dropdownItem.addEventListener("click", function(e) {
            const selectedText = e.target.textContent
            const parentDropdown = e.target.closest(".dropdown")
            const textInputName = parentDropdown.id.replace("-dropdown", "")

            const associatedTextInput = e.target.closest("form").querySelector(`input[name="${textInputName}"]`)

            associatedTextInput.value = selectedText
            associatedTextInput.select()
            associatedTextInput.setSelectionRange(selectedText.length, selectedText.length)

            parentDropdown.classList.remove("is-active")
        })
    }
}


async function autocompleteTextInputScrollHandler(event) {
    if (!([38, 40].includes(event.keyCode))) {
        return  // exit if key is not up or down arrow
    }

    const dropdown = event.target.closest("form").querySelector(".dropdown.text-input-dropdown")
    
    if (!(dropdown.classList.contains("is-active"))) {
        return
    }

    const selectElements = dropdown.querySelectorAll(".dropdown-item")

    console.log(dropdown)
    console.log(selectElements)
}


async function queryIngredientNames(searchTerm, csrfToken=null) {
    const url = `/pantry/ingredients/search`

    const response = {}

    if (csrfToken == null) {
        response.message = "queryIngredientNames | Please provide a csrfToken."
        console.log(response.message)

        return response
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                search_term: searchTerm
            })
        })
    
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
        }
  
        const json = await response.json()

        response.success = true
        response.data = json

        return response

    } catch (error) {
        response.message = error.message
        console.error(error.message)

        return response
    }
}