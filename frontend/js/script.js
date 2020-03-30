const employeeBenefits = 1000;
const dependentBenefits = 500;

var numOfDependents = 0;

function calculate() {
    var benefitTotal = 0;

    var employeeName = document.getElementById("employeeName").value;

    console.log('Calculating total benefits cost for employee: ', employeeName)

    benefitTotal += individualBenefits(employeeName, benefitTotal, false);

    for( var i = 0; i < numOfDependents; i++ ) {
        var dependentName = document.getElementById(`dependent${i}`).value;
        benefitTotal += individualBenefits(dependentName, benefitTotal, true);
    }
    console.log(`benefit total: ${benefitTotal}`)
    document.getElementById("total").innerHTML = benefitTotal;

    $.ajax({
        url: `http://localhost:8080/api/employees/add?name=${employeeName}&benefit_cost=${benefitTotal}`,
        type: 'POST',
        success: function(data) {
            console.log(JSON.stringify(data.name))
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    }); 

    document.getElementById('employeeName').value = ""
    for( var i = 0; i < numOfDependents; i++ ) {
        document.getElementById(`dependent${i}`).value = "";
    }
}

function createTextBoxes() {
    console.log('Creating extra text boxes for dependents')
    var container = document.getElementById("dependentContainer");
    container.innerHTML = "";
    numOfDependents = document.getElementById("numDependents").value;

    if( isNaN(numOfDependents) ) {
	    alert("Please enter a number");
        document.getElementById("numDependents").value = "";
        return;
    }

    for (var i = 0; i < numOfDependents; i++) {
        container.innerHTML += `<br/><input id = \"dependent${i}\" placeholder = \"Name of Dependent\"><br/>`;
    }
    container.innerHTML += `<button onclick=\"calculate()\" id = \"employeeBtn\">Add Employee</button>`;
    document.getElementById("numDependents").value = "";
}

function individualBenefits(name, isDependent) {
    console.log('Calculating benefits for individual: ', name);
    benefitRate = isDependent ? dependentBenefits : employeeBenefits;
    var benefitCost = 0;
    if( name.charAt(0).toLowerCase() == 'a' ) {
        benefitCost += (benefitRate * .9);
    } else {
        benefitCost += benefitRate;
    }
    console.log(`benefits for individual ${name} are ${benefitCost} `);
    return benefitCost;
}

function searchEmployee() {
    var employeeName = document.getElementById("employeeNameSearch").value;
    $.ajax({
        url: `http://localhost:8080/api/employee/benefits?name=${employeeName}`,
        type: 'GET',
        success: function(data) {
            console.log(JSON.stringify(data.name))
            if( data.name === undefined ) {
                alert("No records exist for this Employee yet.")
                document.getElementById("employeeNameSearch").value = "";
                return;
            }
            document.getElementById("benefitTotal").innerHTML = data.name; 
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
}