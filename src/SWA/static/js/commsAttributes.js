// Initial Calls
fetchdata();

function updateTime(){
    $('#time').text(function(){
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        return ("Current Time: " + time + " EST");
    })
}

// Refresh Comms Attributes
function fetchdata(){

    updateTime();

    $.ajax({
        // fo/views.commsFetchdata
        url: 'fetchdata', // comms/fetchdata
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

                // Update Subsystem Telemetry panel
                document.getElementById("Telemetry-ACS").innerText = data['Telemetry-ACS'] ? 'Received' : 'Not Received';
                document.getElementById("Telemetry-EPS").innerText = data['Telemetry-EPS'] ? 'Received' : 'Not Received';
                document.getElementById("Telemetry-TCS").innerText = data['Telemetry-TCS'] ? 'Received' : 'Not Received';
                document.getElementById("Telemetry-Payload").innerText = data['Telemetry-Payload'] ? 'Received' : 'Not Received';

                // Update System Status panel
                document.getElementById("On-Board-Computer").innerText = data['On-Board-Computer'] ? 'Reached' : 'Not Reached';
                document.getElementById("Antenna-Status").innerText = data['Antenna-Status'] ? 'Reached' : 'Not Reached';

                // Update Signal Attributes panel
                document.getElementById("Bandwidth").innerText = data['Bandwidth'];
                document.getElementById("Gain").innerText = data['Gain'];

                // Update Mission Objective panel
                document.getElementById("Target").innerText = data['Target'] ? 'Reached' : 'Not Reached';
                document.getElementById("Image").innerText = data['Image'] ? 'Captured' : 'Not Captured';
                document.getElementById("Status").innerText = data['Status'] ? 'Completed' : 'Not Completed';

            }
        }
    });
}

// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,1000);
});