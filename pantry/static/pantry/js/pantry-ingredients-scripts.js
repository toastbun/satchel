for (let deleteButton of document.querySelectorAll(".list-item-delete")) {
    deleteButton.addEventListener("click", deleteButtonClickHandler)
}

async function deleteButtonClickHandler(e) {
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

async function deleteRecord(recordId, csrftoken=null) {
    const url = "/pantry/ingredients/delete";

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