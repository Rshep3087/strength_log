function precise(x) {
    return Math.round(x * 2) / 2;
}

function calculateMax() {
    const weight = Number(document.getElementById("weightLifted").value);
    const reps = Number(document.getElementById("repsCompleted").value);

    const table = document.getElementById("max-rep-table");

    const oneRepDisplay = document.getElementById("one-rep-max");
    const oneRepDisplayUnit = document.getElementById("units");

    oneRepMax = weight * (1 + (reps / 30));
    twoRepMax = oneRepMax * 0.97
    threeRepMax = oneRepMax * 0.94
    fourRepMax = oneRepMax * 0.92
    fiveRepMax = oneRepMax * 0.89

    table.rows[1].cells[1].innerHTML = precise(oneRepMax);
    table.rows[2].cells[1].innerHTML = precise(twoRepMax);
    table.rows[3].cells[1].innerHTML = precise(threeRepMax);
    table.rows[4].cells[1].innerHTML = precise(fourRepMax);
    table.rows[5].cells[1].innerHTML = precise(fiveRepMax);

    oneRepDisplay.innerHTML = `Your One-Rep Max: ${precise(oneRepMax)}`;
    oneRepDisplayUnit.classList.remove('invisible');
}
