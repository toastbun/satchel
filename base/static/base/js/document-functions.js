function getCsrfTokenFromPage() {
    try {
        return document.querySelector("[data-token]").dataset.token
    } catch (error) {
        console.log(`getCsrfTokenFromPage | Error: No element was found on the document with a "data-token" attribute.`)

        return null
    }
}


function toggleSectionVisibility(section=null, force=null) {
    /**
     * Toggles an element's visibility by adding or removing a special CSS class that changes the element's display value to none.
     * Force a state by using the force parameter (valid force parameters are "hide" and "show").
     */
    if (section == null) {
        const errorMessage = `Please provide an Element.`
        console.log(`toggleSectionVisibility | Error: ${errorMessage}`)

        // throw Error(errorMessage)
    }

    const inactiveClassName = "section-inactive"

    if (force == null) {
        section.classList.contains(inactiveClassName) ? section.classList.remove(inactiveClassName) : section.classList.add(inactiveClassName)
    } else if (force == "hide") {
        if (!(section.classList.contains(inactiveClassName))) {
            section.classList.add(inactiveClassName)
        } else {
            console.log(`toggleSectionVisibility | Warning: Attempted to hide an element that already has the "${inactiveClassName}" class.`)
        }
    } else if (force == "show") {
        if (section.classList.contains(inactiveClassName)) {
            section.classList.remove(inactiveClassName)
        } else {
            console.log(`toggleSectionVisibility | Warning: Attempted to show an element that does not have the "${inactiveClassName}" class.`)
        }
    } else {
        const errorMessage = `Use force="show" or force="hide", not force="${force}".`
        console.log(`toggleSectionVisibility | Error: ${errorMessage}`)

        // throw Error(errorMessage)
    }
}


async function togglePropertiesEditability(elementsList=null, force=null) {
    /**
     * Toggles a list of elements between "editable" and "non-editable".
     * An "editable" element is a text field, dropdown, datepicker, etc.
     * A "non-editable" field is strictly text or visual content without input.
     * Force a state by using the force parameter (valid force parameters are "on" and "off").
     */
    if (elementsList == null) {
        const errorMessage = `Please provide a list of elements whose properties editability should be toggled.`
    
        throw Error(`togglePropertiesEditability | Error: ${errorMessage}`)
    }

    elementsList = Array.from(elementsList)  // change to Array in order to use .some()

    const csrfToken = getCsrfTokenFromPage()

    nullValue = "---------"

    if ((force == "on" && force != "off") || elementsList.every((element) => !element.classList.contains("editability-active"))) {
        // force is "on" OR no elements contain ".editability-active"
        // off --> on

        for (element of elementsList) {
            // do stuff
            const property = element.dataset.prop
            const inputType = element.dataset.inputtype
            const value = element.innerText

            // <input type="text">
            // select.options[select.selectedIndex].value

            if (inputType == "text") {
                element.innerText = null
                element.innerHTML = `<input type="text" class="input" value="${value}" />`
            } else if (inputType == "select") {
                let data = []

                if (property == "grocery_type") {
                    let groceryTypes = localStorage.getItem("groceryTypes")

                    if (groceryTypes) {
                        data = groceryTypes.split(",")
                    } else {
                        response = await getGroceryTypes(true, csrfToken)
                        groceryTypes = response.data

                        localStorage.setItem("groceryTypes", groceryTypes)
                        data = groceryTypes
                    }
                } else if (property == "substitute_key") {
                    let foodSubstitutes = localStorage.getItem("foodSubstitutes")

                    if (foodSubstitutes) {
                        data = foodSubstitutes.split(",")
                    } else {
                        response = await getFoodSubstitutes(true, csrfToken)
                        foodSubstitutes = response.data

                        localStorage.setItem("foodSubstitutes", foodSubstitutes)
                        data = foodSubstitutes
                    }
                }

                element.innerText = null

                let selectHTML = `<span class="select"><select id="${property}-input">`

                for (let selectValue of data) {
                    selectHTML = `${selectHTML}<option value="${selectValue ? selectValue : null}" ${selectValue == value ? "selected" : ""}>${selectValue ? selectValue : nullValue}</option>`
                }

                 element.innerHTML = `${selectHTML}</select></span>`
            } else {
                throw Error(`togglePropertiesEditability | Error: element for property ${property} does not have a valid inputtype data attribute: ${inputType}`)
            }

            element.classList.add("editability-active")
        }
    } else if ((force == "off" && force != "on") || elementsList.every((element) => element.classList.contains("editability-active"))) {
        // force is "off" or all elements contain ".editability-active"
        // on --> off
        for (element of elementsList) {
            // do stuff
            const property = element.dataset.prop
            const inputType = element.dataset.inputtype
            const value = element.innerText

            if (inputType == "text") {
                element.innerText = element.querySelector("input").value
            } else if (inputType == "select") {
                // console.log(element)
                const selectedValue = element.querySelector(".select select").value
                element.innerText = selectedValue == "null" ? "N/A" : selectedValue
            } else {
                throw Error(`togglePropertiesEditability | Error: element for property ${property} does not have a valid inputtype data attribute: ${inputType}`)
            }

            element.classList.remove("editability-active")
        }
    } else {
        throw Error("UH OHHHHH FIGURE DIS OUT")
    }
}



function toggleEditTrashIcon(icon=null, force=null) {
    /**
     * Toggles a provided icon between edit and trash.
     * Force a state by using the force parameter (valid force parameters are "edit" and "trash").
     */
    if (icon == null) {
        const errorMessage = `Please provide an icon Element.`
        console.log(`toggleEditTrashIcon | Error: ${errorMessage}`)

        // throw Error(errorMessage)
    }

    const editClassName = "fa-pen-to-square"
    const trashClassName = "fa-trash-can"

    if ((force == "edit" && force != "trash") || icon.classList.contains(trashClassName)) {
        icon.classList.remove(trashClassName)
        icon.classList.add(editClassName)
    } else if ((force == "trash" && force != "edit") || icon.classList.contains(editClassName)) {
        icon.classList.remove(editClassName)
        icon.classList.add(trashClassName)
    } else {
        if (force == null) {
            console.log(`toggleEditTrashIcon | Warning: Attempted to toggle an icon that has neither the "${editClassName}" or "${trashClassName}" classes.`)
        } else {
            const errorMessage = `Use force="edit" or force="trash", not force="${force}".`
            console.log(`toggleEditTrashIcon | Error: ${errorMessage}`)
    
            // throw Error(errorMessage)
        }
    }
}