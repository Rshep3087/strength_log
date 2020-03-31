let main_sets_id = 0;
let accessory_sets_id = 0;


function remove() {
    if (main_sets_id < 1) {

    } else {
        let set = document.getElementById("main-" + main_sets_id + "-form");
        set.remove();

        main_sets_id--;
    }

}


function add() {
    main_sets_id++; // increment main_sets_id to get a unique ID for the new element

    let templateForm = document.getElementById("main-_-form");

    let newForm = templateForm.cloneNode(true);

    newForm.setAttribute("id", newForm.getAttribute("id").replace("_", main_sets_id));
    newForm.setAttribute("data-index", main_sets_id);

    let inputElements = newForm.getElementsByTagName("input");
    let labelElement = newForm.getElementsByTagName("label");

    labelElement[0].setAttribute("id", labelElement[0].getAttribute("id").replace("_", main_sets_id));
    labelElement[0].innerHTML = "Set: " + (main_sets_id + 1).toString();

    for (i = 0; i < inputElements.length; i++) {
        inputElements[i].setAttribute("id", inputElements[i].getAttribute("id").replace("_", main_sets_id));
        inputElements[i].setAttribute("name", inputElements[i].getAttribute("name").replace("_", main_sets_id));
    }

    newForm.setAttribute("class", "subform")

    let sets = document.getElementById("main-subform-container");

    //append elements
    sets.appendChild(newForm);

}

function remove_accessory() {
    if (accessory_sets_id < 1) {

    } else {
        let set = document.getElementById("accessories-" + accessory_sets_id + "-form");
        set.remove();

        accessory_sets_id--;
    }

}

function add_accessory() {
    accessory_sets_id++; // increment accessory_sets_id to get a unique ID for the new element

    let templateForm = document.getElementById("accessories-_-form");

    let newForm = templateForm.cloneNode(true);

    newForm.setAttribute("id", newForm.getAttribute("id").replace("_", accessory_sets_id));
    newForm.setAttribute("data-index", accessory_sets_id);

    let inputElements = newForm.getElementsByTagName("input");
    let accessoryToAdd = document.getElementById("accessory-lift");

    inputElements[0].value = accessoryToAdd.value;

    for (i = 0; i < inputElements.length; i++) {
        inputElements[i].setAttribute("id", inputElements[i].getAttribute("id").replace("_", accessory_sets_id));
        inputElements[i].setAttribute("name", inputElements[i].getAttribute("name").replace("_", accessory_sets_id));
    }

    newForm.setAttribute("class", "subform");

    let sets = document.getElementById("accessories-subform-container");

    //append elements
    sets.appendChild(newForm);

}