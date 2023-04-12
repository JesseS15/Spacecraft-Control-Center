window.setInterval(function(){
    $('#time').text(function(){
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        return ("Current Time: " + time + " EST");
    })
}, 1000)

window.setInterval(function(){
    var active = true;
    $('.signalacs').css('border-color', function(){
        if (active = true) {
            return 'green';
        } else {
            return 'red';
        }
    }).text(function(){
        if (active = true) {
            return "Active";
        } else {
            return "InActive";
        }
    });
}, 1000);

window.setInterval(function(){
    var active1 = true;
    $('.verifyacs').css('border-color', function(){
        if (active1 = true) {
            return 'green';
        } else {
            return 'red';
        }
    }).text(function(){
        if (active = true) {
            return "Signal Verified";
        } else {
            return "Signal Not Verified";
        }
    });
}, 1000);

window.setInterval(function(){
    var active1 = true;
    $('.acstelemtry').css('border-color', function(){
        if (active1 = true) {
            return 'red';
        } else {
            return 'green';
        }
    }).text(function(){
        if (active = true) {
            return "Not Transfering";
        } else {
            return "Transfering in Progress";
        }
    });
}, 1000);

// Refresh Payload Attributes
function fetchdata(){
    $.ajax({
        // fo/views.payloadFetchdata
        url: 'fetchdata', // payload/fetchdata
        type: 'GET',
        dataType: 'json',

        success: (data) => {
            //Debug return data
            console.log(data);
    
            if (Object.keys(data).length > 0){
                // Update Orientation panel
                //document.getElementById("Oreintation-Roll").innerText = data['roll'];
                //document.getElementById("Oreintation-Pitch").innerText = data['pitch'];
                //document.getElementById("Oreintation-Yaw").innerText = data['yaw'];
                //document.getElementById("Oreintation-Longitude").innerText = data['longitude'];
            }
        }
    });
}

// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,5000);
});