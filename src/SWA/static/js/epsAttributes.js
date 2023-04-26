// Initial Calls
updateTelemetry(false);
fetchdata();

function updateTime(){
    $('#time').text(function(){
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        return ("Current Time: " + time + " EST");
    })
}
function updateTelemetry(telemetryTransferring){
    $('.epstelemtry').css('border-color', function(){
        if (telemetryTransferring == true) {
            return 'green';
        } else {
            return 'red';
        }
    }).text(function(){
        if (telemetryTransferring == true) {
            return "Transferring in Progress";
        } else {
            return "Not Transferring";
        }
    });
}

// Refresh EPS Attributes
function fetchdata(){

    updateTime();

    $.ajax({
        // fo/views.epsFetchdata
        url: 'fetchdata', // eps/fetchdata
        type: 'GET',
        dataType: 'json',

        success: (data) => {
            //Debug return data
            //console.log(data);
    
            if (Object.keys(data).length > 0){

                // Update terminal with console log data
                if('consoleLog' in  data){
                    if (data['consoleLog'].length > terminal2.childElementCount){
                        // Clear right terminal and append subsystem command log
                        terminal2.innerText = '';
                        for (var i = 0; i < data['consoleLog'].length; i++) {
                            const output = document.createElement('p');
                            output.textContent = `${data['consoleLog'][i]}`;
                            terminal2.appendChild(output);
                        }
                        terminal2.parentElement.scrollTop = terminal2.parentElement.scrollHeight;
                    }
                }
                
                // Update Power Distribution panel
                document.getElementById("ACS-Percent").innerText = data['acs_power'];
                document.getElementById("ACS-Watts").innerText = data['acs_power'] * 10;
                document.getElementById("EPS-Percent").innerText = data['eps_power'];
                document.getElementById("EPS-Watts").innerText = data['eps_power'] * 10;
                document.getElementById("TCS-Percent").innerText = data['tcs_power'];
                document.getElementById("TCS-Watts").innerText = data['tcs_power'] * 10;
                document.getElementById("COMMs-Percent").innerText = data['comms_power'];
                document.getElementById("COMMs-Watts").innerText = data['comms_power'] * 10;
                document.getElementById("Payload-Percent").innerText = data['payload_power'];
                document.getElementById("Payload-Watts").innerText = data['payload_power'] * 10;

                // Update Power Generated Panel
                document.getElementById("Panel-Articulation").innerText = data['articulation'];
                document.getElementById("Total-Percent").innerText = data['total_power'];
                document.getElementById("Total-Watts").innerText = data['total_power'] * 10;

                // Update Batery Panel
                document.getElementById("In-Use-Percent").innerText = data['total_power'];
                document.getElementById("In-Use-Watts").innerText = data['total_power'] * 10;

                // Update Telemetry panel
                updateTelemetry(data['telemetry_Transferring']);
                document.getElementById("Telemetry-Status").innerText = data['telemetry_Transferred'] ? 'Transferred' : 'Not Transferred';
            }
        }
    });
}

// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,1000);
});