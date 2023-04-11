window.setInterval(function(){
    $('#time').text(function(){
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        return ("Current Time: " + time + " EST");
    })
}, 1000)

window.setInterval(function(){
    var active = true;
    $('.signaleps').css('border-color', function(){
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
    $('.verifyeps').css('border-color', function(){
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
    $('.epstelemtry').css('border-color', function(){
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

// Refresh SimCraft Attributes
function fetchdata(){
    $.ajax({
        // fo/views.epsFetchdata
        url: 'fetchdata', // eps/fetchdata
        type: 'GET',
        dataType: 'json',

        success: (data) => {
    
          console.log(data)
        }
    });
}

// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,5000);
});