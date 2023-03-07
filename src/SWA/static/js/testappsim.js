// fosim.js
// Purpose: Refresh simcraft attributes and submit flight operator inputs on the fo sim page.

const terminal1 = document.getElementById('terminal1');
const terminal2 = document.getElementById('terminal2');
const input = document.getElementById('input');

fetchdata();

input.addEventListener('keyup', function (event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    const command = this.value.trim();
    this.value = '';
    const output = document.createElement('p');
    output.textContent = `$ ${command}`;
    terminal2.appendChild(output);
    terminal2.parentElement.scrollTop = terminal2.parentElement.scrollHeight;

    $.ajax(
        {
            // fo/views.submit
            url: 'submit',
            type: 'GET',
            //dataType: 'json',
            data:{
                cmd: command,
            },
    
            success: function( data )
            {
                console.log("js " + data);
            }
         })
  }
});

// Resize

const resizable = document.querySelector('.resizable');
const handle = document.querySelector('.resizable-handle');

handle.addEventListener('mousedown', initResize);

function initResize(e) {
  e.preventDefault();
  window.addEventListener('mousemove', resize);
  window.addEventListener('mouseup', stopResize);
}

function resize(e) {
  resizable.style.height = `${window.innerHeight - e.clientY}px`;
}

function stopResize(e) {
  window.removeEventListener('mousemove', resize);
  window.removeEventListener('mouseup', stopResize);
}

// Refresh SimCraft Attributes
function fetchdata(){
    $.ajax({
        // fo/views.fetchdata
        url: 'fetchdata',
        type: 'GET',
        dataType: 'json',

        success: (data) => {
          if (data.length > terminal1.children.length){
            terminal1.replaceChildren();
            for (var i = 0; i < data.length; i++) {
              const output = document.createElement('p');
              output.textContent = `$ ${data[i]}`;
              terminal1.appendChild(output);
            }
            terminal1.parentElement.scrollTop = terminal1.parentElement.scrollHeight;
            console.log(data);
          }
        }
    });
}
// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,5000);
});