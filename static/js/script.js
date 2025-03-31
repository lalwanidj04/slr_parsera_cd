function uploadGrammar() {
    let grammarInput = document.getElementById("grammarInput").value.trim().split("\n");

    grammarInput = grammarInput.filter(line => line.trim() !== "");

    fetch("/upload_grammar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ grammar: grammarInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Uploaded Grammar:", JSON.stringify(data.grammar, null, 2));
        alert(data.message);
    })
    .catch(error => console.error("Error:", error));
}


function uploadTable() {
    let tableInput = document.getElementById("tableInput").value.trim();

    try {
        let tableData = JSON.parse(tableInput);

        console.log("Parsed Table (Before Sending):", tableData);

        fetch("/upload_table", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ table: tableData })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Uploaded Parsing Table (Server Response):", data.table);
            alert(data.message);
        })
        .catch(error => console.error("Error:", error));

    } catch (e) {
        alert("Invalid JSON format");
    }
}



let parsingSteps = [];
let currentStep = 0;

document.getElementById("parseForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let inputString = document.getElementById("inputString").value;

    fetch("/parse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_string: inputString })
    })
    .then(response => response.json())
    .then(data => {
        parsingSteps = data.steps;
        currentStep = 0;
        document.getElementById("parserControls").style.display = "block";
        updateTable();
    })
    .catch(error => console.error("Error:", error));
});

document.getElementById("nextStep").addEventListener("click", function() {
    if (currentStep < parsingSteps.length - 1) {
        currentStep++;
        updateTable();
    } else {
        alert("Parsing Completed!");
    }
});

function updateTable() {
    let tableBody = document.querySelector("#parsingTable tbody");
    tableBody.innerHTML = "";

    for (let i = 0; i <= currentStep; i++) {
        let step = parsingSteps[i];
        let row = `<tr>
            <td>${step.stack.join(" ")}</td>
            <td>${step.remaining_input}</td>
            <td>${step.action}</td>
        </tr>`;
        tableBody.innerHTML += row;
    }
}

function restartParsing() {
    currentStep = 0;
    updateTable();
}
