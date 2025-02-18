document.addEventListener("DOMContentLoaded", (event) => {
    const ingredientNameInput = document.querySelector("#id_food_substitute")
    const ingredientNameInputContainer = ingredientNameInput.parentNode.parentNode

    const foodSubstituteDropdown = document.querySelector("#food_substitute-dropdown")

    ingredientNameInputContainer.after(foodSubstituteDropdown)

    foodSubstituteDropdown.style.top = "-12px"
    foodSubstituteDropdown.style.position = "relative"
    foodSubstituteDropdown.style.width = "100%"
    foodSubstituteDropdown.querySelector(".dropdown-menu").style.width = "100%"

    for (let deleteButton of document.querySelectorAll(".list-item-delete")) {
        deleteButton.addEventListener("click", deleteButtonClickHandler)
    }

    for (let textInputFieldWithAutocomplete of document.querySelectorAll(".autocomplete")) {
        textInputFieldWithAutocomplete.addEventListener("input", autocompleteTextInputUpdateHandler)
    }
})

/** function definitions **/

function getCsrfTokenFromForm(formElement) {
    return formElement.closest("form").querySelector("[name='csrfmiddlewaretoken']").value
}

function getAssociatedDropdown(formElement) {
    return formElement.closest("form").querySelector(`#${formElement.name}-dropdown`)
}

async function deleteButtonClickHandler(e) {
    deleteConfirmButtonClickHandler(e)
}

async function autocompleteTextInputUpdateHandler(e) {
    const csrfToken = getCsrfTokenFromForm(e.target)
    const foodSubstitutes = await queryFoodSubstitutes(e.target.value, csrfToken)
    const dropdown = getAssociatedDropdown(e.target)

    if (!(dropdown.classList.contains("is-active"))) {
        dropdown.classList.add("is-active")
    } else {
        if (e.target.value == "") {
            dropdown.classList.remove("is-active")
        }
    }

    const dropdownContent = dropdown.querySelector(".dropdown-content")

    dropdownContent.replaceChildren()

    if (foodSubstitutes.data.length) {
        for (let foodSubstitute of foodSubstitutes.data) {
            const newSelectElement = document.createElement("div")
            const newSelectElementText = document.createTextNode(foodSubstitute)
    
            newSelectElement.classList.add("dropdown-item", "unselectable")
            newSelectElement.appendChild(newSelectElementText)

            dropdownContent.appendChild(newSelectElement)
        }
    } else {
        dropdown.classList.remove("is-active")
    }

    for (let dropdownItem of document.querySelectorAll(".dropdown-item")) {
        dropdownItem.addEventListener("mouseover", function(e) {
            e.target.style.backgroundColor = HOVER_COLOR
        })

        dropdownItem.addEventListener("mouseout", function(e) {
            e.target.style.backgroundColor = ""
        })

        dropdownItem.addEventListener("click", function(e) {
            const selectedText = e.target.textContent
            const parentDropdown = e.target.closest(".dropdown")
            const textInputName = parentDropdown.id.replace("-dropdown", "")  // "food_substitute-dropdown"

            const associatedTextInput = e.target.closest("form").querySelector(`input[name="${textInputName}"]`)

            associatedTextInput.value = selectedText
            associatedTextInput.select()
            associatedTextInput.setSelectionRange(selectedText.length, selectedText.length)

            parentDropdown.classList.remove("is-active")
        })
    }
}

async function deleteConfirmButtonClickHandler(e) {
    const recordElement = e.target.closest(".list-item-delete")
    const recordId = recordElement.dataset.id

    const list = recordElement.closest(".list-section")
    const csrftoken = list.dataset.token

    const deleteRecordResponse = await deleteRecord(recordId, csrftoken)

    if (deleteRecordResponse.success) {
        removeElementFromListOnPage("list-ingredients-container", recordId)
    }

    return deleteRecordResponse
}

async function queryFoodSubstitutes(searchTerm, csrftoken=null) {
    const url = `/pantry/food_substitutes/search`

    const response = {}

    if (csrftoken == null) {
        response.message = "queryFoodSubstitutes | Please provide a csrftoken."
        console.log(response.message)

        return response
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
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

async function deleteRecord(recordId, csrftoken=null) {
    const url = "/pantry/ingredients/delete"

    const response = {}

    if (csrftoken == null) {
        response.message = "deleteRecord | Please provide a csrftoken."
        console.log(response.message)

        return response
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                record_id: recordId
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

function removeElementFromListOnPage(listContainerName, recordId) {
    const listContainer = document.querySelector(`.${listContainerName}`)

    const elementToRemove = listContainer.querySelector(`[data-id="${recordId}"]`)

    elementToRemove.closest(".list-item-container").remove()
}

