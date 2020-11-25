let mainSetsID = 0;
let accessorySetsID = 0;


function remove() {
    let mainSetsID = document.getElementById("main-subform-container").lastElementChild.getAttribute("data-index");

    if (mainSetsID >= 1) {
        let set = document.getElementById("set-" + mainSetsID + "-form");
        console.log(set)
        set.remove();
        mainSetsID--;
    }
}


function add() {
    let mainSetsID = document.getElementById("main-subform-container").lastElementChild.getAttribute("data-index");
    mainSetsID++; // increment mainSetsID to get a unique ID for the new element
    console.log(mainSetsID)

    let templateForm = document.getElementById("set-_-form");
    let newForm = templateForm.cloneNode(true);

    newForm.setAttribute("id", newForm.getAttribute("id").replace("_", mainSetsID));
    newForm.setAttribute("data-index", mainSetsID);

    let inputElements = newForm.getElementsByTagName("input");
    let labelElement = newForm.getElementsByTagName("label");

    labelElement[0].setAttribute("id", labelElement[0].getAttribute("id").replace("_", mainSetsID));
    labelElement[0].innerHTML = "Set: " + (mainSetsID + 1).toString();

    for (i = 0; i < inputElements.length; i++) {
        inputElements[i].setAttribute("id", inputElements[i].getAttribute("id").replace("_", mainSetsID));
        inputElements[i].setAttribute("name", inputElements[i].getAttribute("name").replace("_", mainSetsID));
        inputElements[i].setAttribute("type", "number");
    }

    newForm.setAttribute("class", "subform")

    let sets = document.getElementById("main-subform-container");

    //append elements
    sets.appendChild(newForm);
}

function remove_accessory() {
    let accessorySetsID = 0;
    try {
        accessorySetsID = document.getElementById("accessories-subform-container").lastElementChild.getAttribute("data-index");
    }
    catch (e) {
        console.log(e)
        accessorySetsID = -1
    }
    finally {
        console.log(accessorySetsID)

        if (accessorySetsID > -1) {
            let set = document.getElementById("accessories-" + accessorySetsID + "-form");
            set.remove();
            accessorySetsID--;
        }
    }
}

function add_accessory() {
    let accessorySetsID = 0;

    try {
        accessorySetsID = document.getElementById("accessories-subform-container").lastElementChild.getAttribute("data-index");
    }
    catch (error) {
        accessorySetsID = -1;
    }
    accessorySetsID++; // increment accessorySetsID to get a unique ID for the new element

    let templateForm = document.getElementById("accessories-_-form");

    let newForm = templateForm.cloneNode(true);

    newForm.setAttribute("id", newForm.getAttribute("id").replace("_", accessorySetsID));
    newForm.setAttribute("data-index", accessorySetsID);

    let inputElements = newForm.getElementsByTagName("input");
    let accessoryToAdd = document.getElementById("accessory-lift");

    // let accessoryLifts = document.getElementById("accessory-lift").options

    inputElements[0].value = accessoryToAdd.value;

    for (i = 0; i < inputElements.length; i++) {
        inputElements[i].setAttribute("id", inputElements[i].getAttribute("id").replace("_", accessorySetsID));
        inputElements[i].setAttribute("name", inputElements[i].getAttribute("name").replace("_", accessorySetsID));
        if (inputElements[i].readOnly != true) {
            inputElements[i].setAttribute("type", "number");
        }
    }

    newForm.setAttribute("class", "subform");

    let sets = document.getElementById("accessories-subform-container");

    //append elements
    sets.appendChild(newForm);
}