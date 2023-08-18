
function calculate(operand1, operator, operand2) {

    // Gets the CSRF token
    let token = document.getElementById("token").cloneNode(true).firstElementChild;

    // Creates the form
    let form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "addExpression");

    // This is just for reference on how the form would look since the code is hard to read. \\

    // form.innerHTML = `
    //     <button type="submit">Save</button>
    //     <span class="expression"> ${operand1} ${operator} ${operand2} = ${eval(operand1 + operator + operand2)} </span>
    //     <button type="button">Delete</button>
    //     <input type="hidden" name="op1" value=${operand1} />
    //     <input type="hidden" name="operator" value=${operator} />
    //     <input type="hidden" name="op2" value=${operand2} />
    //     <input type="hidden" name="result" value="${eval(operand1 + operator + operand2)}" />
    //     <input type="hidden" name="csrftoken" value=${token}>
    // `

    // Creates the save button
    let saveButton = document.createElement("button");
    saveButton.innerHTML = "Save";
    saveButton.setAttribute("type", "submit");

    let isDisabled = false;


    // Creates the span that goes between the save and delete button
    let content = document.createElement("span");
    content.className = "expression";
    // !!! We'll set the spans innerHTML later once we have checked the users input. !!!


    // Creates the delete button
    let deleteButton = document.createElement("button");
    deleteButton.innerHTML = "Delete";
    deleteButton.setAttribute("type", "button");

    // Checks for possible errors on the users side
    if ((operand1.length === 0) || (operand2.length === 0)) {
        saveButton.setAttribute("disabled", "true");
        isDisabled = true;
        content.innerHTML = "Error: Missing one or both operands! Very icky, no good!";
    }
    else if (isNaN((parseFloat(operand1))) || (isNaN(parseFloat(operand2)))) {
        saveButton.setAttribute("disabled", "true");
        isDisabled = true;
        content.innerHTML = "Error: You have managed to choose an operand that is not a number! Very icky, no good!";
    }
    else if (!['+', '-', '*', '/', '%', '**'].includes(operator.symbol)) {
        saveButton.setAttribute("disabled", "true");
        isDisabled = true;
        content.innerHTML = "Error: You have somehow entered an invalid operator! Very icky, no good!";
    }


    // Sets the forms class based on the validity of the input.
    if (isDisabled) {
        form.className = "red stuff-box";
        form.appendChild(saveButton);
        form.appendChild(content);
        form.appendChild(deleteButton);
    }
    else {
        form.className = "cyan stuff-box";

        let equationResult = eval("(" + operand1 + ")" + (operator.symbol) + "(" + (operand2) + ")");
        if (isNaN(equationResult) || !(isFinite(equationResult))) {
            equationResult = "undefined"
        }

        content.innerHTML = operand1 + " " + operator.symbol + " " + operand2 + " = " + equationResult;

        //Creates all the hidden inputs
        const op1 = document.createElement("input");
        op1.setAttribute("type", "hidden");
        op1.setAttribute("name", "op1");
        op1.setAttribute("value", operand1);

        const operatr = document.createElement("input");
        operatr.setAttribute("type", "hidden");
        operatr.setAttribute("name", "operator");
        operatr.setAttribute("value", (operator.symbol + " " + operator.name));

        const op2 = document.createElement("input");
        op2.setAttribute("type", "hidden");
        op2.setAttribute("name", "op2");
        op2.setAttribute("value", operand2);

        const result = document.createElement("input");
        result.setAttribute("type", "hidden");
        result.setAttribute("name", "result");
        result.setAttribute("value", equationResult);

        const csrftoken = document.createElement("input");
        csrftoken.setAttribute("type", "hidden");
        csrftoken.setAttribute("name", "csrfmiddlewaretoken");
        csrftoken.setAttribute("value", token.value);


        // Adds all the created elements onto the form
        form.appendChild(saveButton);
        form.appendChild(content);
        form.appendChild(deleteButton);
        form.appendChild(op1);
        form.appendChild(operatr);
        form.appendChild(op2);
        form.appendChild(result);
        form.appendChild(csrftoken);

    }

    deleteButton.addEventListener("click", () => {
        form.remove();
    });

    document.getElementById("fresh-expressions-box").appendChild(form);

};


document.getElementById("calculate-button").addEventListener("click", () => {

    const operatorSelector = document.getElementById("operator-select");
    const operand1 = document.getElementById("firstNum").value;
    
    const operator = {
        symbol: operatorSelector.options[operatorSelector.selectedIndex].text,
        name: operatorSelector.value
    };
    const operand2 = document.getElementById("secondNum").value;

    calculate(operand1, operator, operand2);
    return;
});

