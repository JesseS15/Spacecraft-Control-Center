// fosim.js
// Purpose: Refresh simcraft attributes and submit flight operator inputs on the fo sim page.

fetchdata();

// Submit Subsystem Input
$('.submit').click(function(){
    var pk;
    var val;
    pk  = $(this).attr('id');
    cb = document.getElementById($(this).attr("syscheck-id"));
    val = cb.checked;
    $.ajax(
    {
        // fo/views.submit
        url: 'submit',
        type: 'GET',
        dataType: 'json',
        data:{
            syspk: pk,
            value: val,
        },

        success: function( data )
        {
            cb.checked = data;
        }
     })
});

// Refresh SimCraft Attributes
function fetchdata(){
    $.ajax({
        // fo/views.fetchdata
        url: 'fetchdata',
        type: 'GET',
        dataType: 'json',

        success: (data) => {
            // All syscheck checkbox elements in the document
            const collection = document.getElementsByClassName("syscheck");
            for (let i = 0; i < collection.length; i++) {

                let sysvalue = data[collection[i].id];
                // Set checkbox to subsystem value found in database
                collection[i].checked = sysvalue;
                console.log(collection[i].value);
                // Set parent div background color
                if(sysvalue) {
                    collection[i].parentElement.parentElement.style.backgroundColor = 'Green';
                }
                else {
                    collection[i].parentElement.parentElement.style.backgroundColor = 'Red';
                }
            }
        }
    });
}
// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,5000);
});