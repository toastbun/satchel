document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded pantry-ingredients-scripts.js")

    // for (let deleteButton of document.querySelectorAll(".list-item-delete")) {
    //     deleteButton.addEventListener("click", deleteButtonClickHandler)
    // }

    for (let textInputFieldWithAutocomplete of document.querySelectorAll(".autocomplete")) {
        textInputFieldWithAutocomplete.addEventListener("input", autocompleteTextInputUpdateHandler)
    }

    // add edit button functionality to show ingredient page
    if (document.querySelector(".item-icon-button-container")) {
        document.querySelector(".item-icon-button-container").addEventListener("click", activateEditSection)
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

// async function deleteButtonClickHandler(event) {
//     deleteConfirmButtonClickHandler(event)
// }

function activateEditSection(event) {
    /**
     * Called once upon first click of the edit icon.
     *  - Change edit icon to trash icon.
     *  - Show the Confirm and Cancel buttons.
     *  - Show the "Editing Ingredient" notice.
     **/
    const target = event.target.closest(".item-icon-button-container")

    target.removeEventListener("click", activateEditSection)
    target.addEventListener("click", trashIconClickHandler)

    // edit --> trash
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="trash")

    // ensure Confirm and Cancel button visibility
    toggleSectionVisibility(document.querySelector(".confirm-section"), force="show")

    // show appropriate notice
    toggleSectionVisibility(document.querySelector(".delete-notice"), force="hide")
    toggleSectionVisibility(document.querySelector(".edit-notice "), force="show")

    // activate button functionality
    // activateConfirmButton()
    activateDeleteButton()
    activateCancelButton()
}

function deactivateEditSection(event) {
    // ??? --> edit
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="edit")

    // ensure no Confirm and Cancel button visibility
    toggleSectionVisibility(document.querySelector(".confirm-section"), force="hide")

    // Delete --> Confirm
    toggleSectionVisibility(document.querySelector(".confirm-container"), force="show")
    toggleSectionVisibility(document.querySelector(".delete-container"), force="hide")

    // hide all notices
    toggleSectionVisibility(document.querySelector(".delete-notice"), force="hide")
    toggleSectionVisibility(document.querySelector(".edit-notice "), force="hide")

    const iconContainer = event.target.closest(".item-container").querySelector(".item-icon-button-container")

    // reset icon click listeners
    iconContainer.removeEventListener("click", editIconClickHandler)
    iconContainer.removeEventListener("click", trashIconClickHandler)
    iconContainer.addEventListener("click", activateEditSection)
}


function editIconClickHandler(event) {
    const target = event.target.closest(".item-icon-button-container")

    // edit --> trash
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="trash")

    // Delete --> Confirm (if necessary)
    toggleSectionVisibility(document.querySelector(".confirm-container"), force="show")
    toggleSectionVisibility(document.querySelector(".delete-container"), force="hide")

    // show appropriate notice
    toggleSectionVisibility(document.querySelector(".delete-notice"), force="hide")
    toggleSectionVisibility(document.querySelector(".edit-notice "), force="show")

    // editIconClickHandler --> trashIconClickHandler
    target.removeEventListener("click", editIconClickHandler)
    target.addEventListener("click", trashIconClickHandler)
}


function trashIconClickHandler(event) {
    const target = event.target.closest(".item-icon-button-container")

    // trash --> edit
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="edit")

    // Confirm --> Delete (if necessary)
    toggleSectionVisibility(document.querySelector(".delete-container"), force="show")
    toggleSectionVisibility(document.querySelector(".confirm-container"), force="hide")

    // show appropriate notice
    toggleSectionVisibility(document.querySelector(".delete-notice"), force="show")
    toggleSectionVisibility(document.querySelector(".edit-notice "), force="hide")

    // trashIconClickHandler --> editIconClickHandler
    target.removeEventListener("click", trashIconClickHandler)
    target.addEventListener("click", editIconClickHandler)
}

function activateDeleteButton() {
    document.querySelector(".button-container .button-delete").addEventListener("click", deleteButtonHandler)
}

function activateCancelButton() {
    document.querySelector(".button-container .button-cancel").addEventListener("click", deactivateEditSection)
}


async function deleteButtonHandler(event) {
    console.log("Deleted!")

    const itemSectionContainer = event.target.closest("[data-id]")
    const recordId = itemSectionContainer.dataset.id
    const csrfToken = itemSectionContainer.dataset.token

    console.log(`recordId: ${recordId}`)
    console.log(`csrfToken: ${csrfToken}`)

    await deleteIngredient(recordId, csrfToken)

    // deactivateEditSection(event)

    location.reload(true)
}

function cancelButtonHandler(event) {
    deactivateEditSection(event)
}


async function autocompleteTextInputUpdateHandler(e) {
    const csrfToken = getCsrfTokenFromForm(e.target)
    const foodSubstitutes = await queryIngredientNames(e.target.value, csrfToken)
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

// async function deleteConfirmButtonClickHandler(e) {
//     const recordElement = e.target.closest(".list-item-delete")
//     const recordId = recordElement.dataset.id

//     const list = recordElement.closest(".list-section")
//     const csrftoken = list.dataset.token

//     const deleteRecordResponse = await deleteIngredient(recordId, csrftoken)

//     if (deleteRecordResponse.success) {
//         removeElementFromListOnPage("list-ingredients-container", recordId)
//     }

//     return deleteRecordResponse
// }

async function queryIngredientNames(searchTerm, csrftoken=null) {
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

async function deleteIngredient(recordId, csrftoken=null) {
    const url = "/pantry/ingredients/delete"

    const response = {}

    if (csrftoken == null) {
        response.message = "deleteRecord | Please provide a csrftoken."
        console.log(response.message)

        return response
    }

    // console.log(`Calling ${url} with ingredient_id ${recordId}`)

    try {
        const response = await fetch(
            url,
            {
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

