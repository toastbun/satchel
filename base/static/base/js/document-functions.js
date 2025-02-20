


function toggleSectionVisibility(section=null, force=null) {
    /**
     * Toggles an element's visibility by adding or removing a special CSS class that changes the element's display value to none.
     * Force a state by using the force parameter (valid force parameters are "hide" and "show").
     */
    if (section == null) {
        const errorMessage = `Please provide an Element.`
        console.log(`toggleSectionVisibility | Error: ${errorMessage}`)

        throw Error(errorMessage)
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

        throw Error(errorMessage)
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

        throw Error(errorMessage)
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
    
            throw Error(errorMessage)
        }
    }
}