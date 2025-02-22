document.addEventListener("DOMContentLoaded", (event) => {
    console.log("Loaded pantry-scripts.js")

    document.querySelector(".page-content").addEventListener("keydown", (event) => {
        if (!([13].includes(event.keyCode))) {
            return  // exit if key is not enter
        }

        const confirmButtonContainer = document.querySelector(".button-confirm-container:not(.section-inactive)")

        if (confirmButtonContainer) {
            const confirmButton = confirmButtonContainer.querySelector("button")

            if (confirmButton.classList.contains("button-update")) {
                confirmButton.click()
            }
        }
    })
})


async function getGroceryTypes(namesOnly=false, csrfToken=null) {
    const url = "/pantry/ingredients/get_grocery_types"

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
                    names: namesOnly
                })
            }
        )

        if (!response.ok) {
            console.log(`getGroceryTypes | Response error: ${response.status}`)
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


async function getFoodSubstitutes(namesOnly=false, csrfToken=null) {
    const url = "/pantry/ingredients/get_food_substitutes"

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
                    names: namesOnly
                })
            })

        if (!response.ok) {
            console.log(`getFoodSubstitutes | Response error: ${response.status}`)
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