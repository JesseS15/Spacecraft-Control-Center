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
function updateTelemetry(telemetryTransfering){
    $('.payloadtelemtry').css('border-color', function(){
        if (telemetryTransfering == true) {
            return 'green';
        } else {
            return 'red';
        }
    }).text(function(){
        if (telemetryTransfering == true) {
            return "Transfering in Progress";
        } else {
            return "Not Transfering";
        }
    });
}

// Refresh Payload Attributes
function fetchdata(){

    updateTime();

    $.ajax({
        // fo/views.payloadFetchdata
        url: 'fetchdata', // payload/fetchdata
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

                // Update Gimbal System panel
                document.getElementById("Connection").innerText = data['Connection'] ? 'Active' : 'Inactive';

                // Update Imager System panel
                document.getElementById("In-Range").innerText = data['In-Range']   ? 'In Range' : 'Not In Range';
                document.getElementById("Target-Acquired").innerText = data['Target-Acquired'] ? 'Acquired' : 'Not Acquired';
                document.getElementById("Image-Recieved").innerText = data['Image-Recieved']     ? 'Recieved' : 'Not Recieved';

                // Update System Status panel
                document.getElementById("Gimbal-Status").innerText = data['Gimbal-Status']   ? 'Active' : 'Inactive';
                document.getElementById("Imager-Status").innerText = data['Imager-Status']   ? 'Active' : 'Inactive';

                // Update Signal Status panel
                document.getElementById("Optical-Electronics").innerText = data['Optical-Electronics']   ? 'Reached' : 'Not Reached';
                document.getElementById("Bus-Connection").innerText = data['Bus-Connection']   ? 'Reached' : 'Not Reached';
                document.getElementById("Gimbal-Connection").innerText = data['Gimbal-Connection']   ? 'Reached' : 'Not Reached';

                // Update Telemetry panel
                updateTelemetry(data['telemetry_transfering']);
                document.getElementById("Telemetry-Status").innerText = data['telemetry_transfered'] ? 'Transfered' : 'Not Transfered';
            }
        }
    });
}

// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,1000);
});