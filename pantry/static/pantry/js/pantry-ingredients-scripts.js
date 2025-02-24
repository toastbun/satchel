document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded pantry-ingredients-scripts.js")

    for (let textInputFieldWithAutocomplete of document.querySelectorAll(".autocomplete")) {
        textInputFieldWithAutocomplete.addEventListener("input", autocompleteTextInputUpdateHandler)
    }

    // add edit button functionality to show ingredient page
    if (document.querySelector(".item-icon-button-container")) {
        document.querySelector(".item-icon-button-container").addEventListener("click", activateEditSection)
    }
})


let initialPropertyValues = {}


/**
 * 
 * functions
 * 
 **/


function getAssociatedDropdown(formElement) {
    return formElement.closest("form").querySelector(`#${formElement.name}-dropdown`)
}


async function activateEditSection(event) {
    /**
     * Called once upon first click of the edit icon.
     *  - Change edit icon to trash icon.
     *  - Show the Confirm and Cancel buttons.
     *  - Show the "Editing Ingredient" notice.
     **/
    const target = event.target.closest(".item-icon-button-container")

    initialPropertyValues = {
        name: document.querySelector(`#ingredient-name-container`).innerText,
        grocery_type: document.querySelector(`#ingredient-grocery_type-container`).innerText,
        substitute_key: document.querySelector(`#ingredient-substitute_key-container`).innerText
    }

    try {
        await togglePropertiesEditability(document.querySelectorAll(".editable-record-property"), force="on")
    } catch (error) {
        console.log(`editIconClickHandler | ${error}`)
    }

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
    activateUpdateButton()
    activateDeleteButton()
    activateCancelButton()
}

async function deactivateEditSection(event) {
    try {
        await togglePropertiesEditability(document.querySelectorAll(".editable-record-property"), force="off")
    } catch (error) {
        console.log(`editIconClickHandler | ${error}`)
    }

    resetEditableProperties()

    // ??? --> edit
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="edit")

    // ensure no Confirm and Cancel button visibility
    toggleSectionVisibility(document.querySelector(".confirm-section"), force="hide")

    // Delete --> Confirm
    toggleSectionVisibility(document.querySelector(".update-container"), force="show")
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


async function editIconClickHandler(event) {
    try {
        await togglePropertiesEditability(document.querySelectorAll(".editable-record-property"), force="on")
    } catch (error) {
        console.log(`editIconClickHandler | ${error}`)
    }

    const target = event.target.closest(".item-icon-button-container")

    // edit --> trash
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="trash")

    // Delete --> Confirm (if necessary)
    toggleSectionVisibility(document.querySelector(".update-container"), force="show")
    toggleSectionVisibility(document.querySelector(".delete-container"), force="hide")

    // show appropriate notice
    toggleSectionVisibility(document.querySelector(".delete-notice"), force="hide")
    toggleSectionVisibility(document.querySelector(".edit-notice "), force="show")

    // editIconClickHandler --> trashIconClickHandler
    target.removeEventListener("click", editIconClickHandler)
    target.addEventListener("click", trashIconClickHandler)
}


function resetEditableProperties() {
    for (let initialProperty of Object.keys(initialPropertyValues)) {
        const initialPropertyValue = initialPropertyValues[initialProperty]
        const editablePropertyContainer = document.getElementById(`ingredient-${initialProperty}-container`)

        editablePropertyContainer.innerText = initialPropertyValue
    }

    console.log(initialPropertyValues)
}


async function trashIconClickHandler(event) {
    try {
        await togglePropertiesEditability(document.querySelectorAll(".editable-record-property"), force="off")
    } catch (error) {
        console.log(`editIconClickHandler | ${error}`)
    }

    resetEditableProperties()

    const target = event.target.closest(".item-icon-button-container")

    // trash --> edit
    toggleEditTrashIcon(document.querySelector(".item-icon-button-container i.fa-regular"), force="edit")

    // Confirm --> Delete (if necessary)
    toggleSectionVisibility(document.querySelector(".delete-container"), force="show")
    toggleSectionVisibility(document.querySelector(".update-container"), force="hide")

    // show appropriate notice
    toggleSectionVisibility(document.querySelector(".delete-notice"), force="show")
    toggleSectionVisibility(document.querySelector(".edit-notice "), force="hide")

    // trashIconClickHandler --> editIconClickHandler
    target.removeEventListener("click", trashIconClickHandler)
    target.addEventListener("click", editIconClickHandler)
}

function activateUpdateButton() {
    document.querySelector(".button-container .button-update").addEventListener("click", updateButtonClickHandler)
}

function activateDeleteButton() {
    document.querySelector(".button-container .button-delete").addEventListener("click", deleteButtonClickHandler)
}

function activateCancelButton() {
    document.querySelector(".button-container .button-cancel").addEventListener("click", cancelButtonClickHandler)
}


async function updateButtonClickHandler(event) {
    console.log("Entered updateButtonClickHandler.")

    const itemSectionContainer = event.target.closest("[data-id]")
    const recordId = itemSectionContainer.dataset.id
    const csrfToken = itemSectionContainer.dataset.token

    const updateData = {}

    for (let inputElement of document.querySelectorAll(".editability-active")) {
        let validated = true

        const property = inputElement.dataset.prop
        const inputType = inputElement.dataset.inputtype

        let selectedValue

        if (inputType == "text") {
            selectedValue = inputElement.querySelector("input").value
        } else if (inputType == "select") {
            selectedValue = inputElement.querySelector(`#${property}-input`).value
        } else {
            validated = false
        }

        updateData[property] = selectedValue
    }

    try {
        await updateIngredient(recordId, updateData, csrfToken)
    } catch(error) {
        console.log(`updateButtonClickHandler | ${error}`)

        return
    }

    location.reload(true)
}


async function deleteButtonClickHandler(event) {
    const itemSectionContainer = event.target.closest("[data-id]")
    const recordId = itemSectionContainer.dataset.id
    const csrfToken = itemSectionContainer.dataset.token

    await deleteIngredient(recordId, csrfToken)

    location.reload(true)
}

async function cancelButtonClickHandler(event) {
    await deactivateEditSection(event)
}


async function autocompleteTextInputUpdateHandler(e) {
    const csrfToken = getCsrfTokenFromPage()
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
            const hoverColor = document.querySelector("[data-theme]").dataset.theme == "dark" ? "hsl(0, 0%, 21%)" : "hsl(0, 0%, 96%)"
            e.target.style.backgroundColor = hoverColor
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


async function queryIngredientNames(searchTerm, csrfToken=null) {
    const url = `/pantry/food_substitutes/search`

    const response = {}

    if (csrfToken == null) {
        response.message = "queryFoodSubstitutes | Please provide a csrfToken."
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
            console.log(`queryIngredientNames | Error: ${response.status}`)
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

async function updateIngredient(recordId, updateData, csrfToken=null) {
    const url = "/pantry/ingredients/update"

    const response = {}

    if (csrfToken == null) {
        console.log(response.message)

        throw Error(response.message)
    }

    try {
        const response = await fetch(
            url,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    record_id: recordId,
                    update_data: updateData
                })
            })

        if (!response.ok) {
            console.log(`updateIngredient | Response error: ${response.status}`)
        }
  
        const json = await response.json()

        response.success = true
        response.data = json

        console.log(`Response:`)
        console.log(response)

        return response

    } catch (error) {
        response.message = error.message
        console.error(error.message)

        return response
    }
}

async function deleteIngredient(recordId, csrfToken=null) {
    const url = "/pantry/ingredients/delete"

    const response = {}

    if (csrfToken == null) {
        response.message = "deleteRecord | Please provide a csrfToken."
        console.log(response.message)

        return response
    }

    try {
        const response = await fetch(
            url,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    record_id: recordId
                })
            })
    
        if (!response.ok) {
            console.log(`deleteIngredient | Error: ${response.status}`)
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

