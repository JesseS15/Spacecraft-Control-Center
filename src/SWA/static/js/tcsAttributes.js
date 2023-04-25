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
    $('.tcstelemtry').css('border-color', function(){
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

// Refresh TCS Attributes
function fetchdata(){

    updateTime();

    $.ajax({
        // fo/views.tcsFetchdata
        url: 'fetchdata', // tcs/fetchdata
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

                // Update ACS Thermals Panel
                document.getElementById("CMG-Temp").innerText = data['CMG-Temp'];
                document.getElementById("Alignment-Temp").innerText = data['Alignment-Temp'];

                // Update EPS Thermals Panel
                document.getElementById("Distribution-Temp").innerText = data['Distribution-Temp'];
                document.getElementById("Battery-Temp").innerText = data['Battery-Temp'];
                document.getElementById("Articulation-Temp").innerText = data['Articulation-Temp'];

                // Update COMMs Thermals Panel
                document.getElementById("Computer-Temp").innerText = data['Computer-Temp'];
                document.getElementById("Processor-Temp").innerText = data['Processor-Temp'];

                // Update Payload Thermals Panel
                document.getElementById("Optical-Temp").innerText = data['Optical-Temp'];
                document.getElementById("Gimbal-Temp").innerText = data['Gimbal-Temp'];
                document.getElementById("Imager-Temp").innerText = data['Imager-Temp'];

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