let sets_id = 0;


function remove() {
    let set = document.getElementById("set-" + sets_id + "-form");
    set.remove();

    sets_id--;
}


function add() {
    sets_id++; // increment sets_id to get a unique ID for the new element

    let templateForm = document.getElementById("set-_-form");

    let newForm = templateForm.cloneNode(true);

    newForm.setAttribute("id", newForm.getAttribute("id").replace("_", sets_id));
    newForm.setAttribute("data-index", sets_id);

    let inputElements = newForm.getElementsByTagName("input");
    let labelElements = newForm.getElementsByTagName("label");

    for (i = 0; i < inputElements.length; i++) {
        inputElements[i].setAttribute("id", inputElements[i].getAttribute("id").replace("_", sets_id));
        inputElements[i].setAttribute("name", inputElements[i].getAttribute("name").replace("_", sets_id));
        labelElements[i].setAttribute("for", labelElements[i].getAttribute("for").replace("_", sets_id));
    }

    newForm.setAttribute("class", "subform")

    console.log(newForm)

    let sets = document.getElementById("subform-container");

    //append elements
    sets.appendChild(newForm);

}