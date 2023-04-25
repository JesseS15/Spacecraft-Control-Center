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
    $('.acstelemtry').css('border-color', function(){
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

// Refresh ACS UI Attributes
function fetchdata(){
    updateTime();

    $.ajax({
        // fo/views.acsFetchdata
        url: 'fetchdata', // acs/fetchdata
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

                // Update Orientation panel
                document.getElementById("Oreintation-Roll").innerText = data['roll'];
                document.getElementById("Oreintation-Pitch").innerText = data['pitch'];
                document.getElementById("Oreintation-Yaw").innerText = data['yaw'];
                document.getElementById("Oreintation-Longitude").innerText = data['longitude'];

                // Update CMG panel
                document.getElementById("CMG-Roll").innerText = data['cmg_roll']   ? 'Active' : 'Inactive';
                document.getElementById("CMG-Pitch").innerText = data['cmg_pitch'] ? 'Active' : 'Inactive';
                document.getElementById("CMG-Yaw").innerText = data['cmg_yaw']     ? 'Active' : 'Inactive';

                // Update Status panel
                document.getElementById("CMG-Status").innerText = data['cmg_status'] ? 'Active' : 'Inactive';
                document.getElementById("Orientation-Relay").innerText = data['orientation_relay'] ? 'Active' : 'Inactive';

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