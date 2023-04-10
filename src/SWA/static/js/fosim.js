// fosim.js
// Purpose: Refresh simcraft attributes and submit flight operator inputs on the fo sim page.

const terminal1 = document.getElementById('terminal1');
const terminal2 = document.getElementById('terminal2');
const input = document.getElementById('input');

fetchdata();
fetchcommands();

input.addEventListener('keyup', function (event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    const command = this.value.trim();
    this.value = '';

    $.ajax(
        {
          // fo/views.submit
          url: '../submit',
          type: 'GET',
          dataType: 'json',
          
          data:{
              cmd: command,
          },

          success: function( data )
          {
            const output = document.createElement('p');
            output.textContent = `$ ${data['consoleCommand']}`;
            terminal2.appendChild(output);
            for (var i = 0; i < data['consoleResponse'].length; i++) {
              const output = document.createElement('p');
              output.textContent = `${data['consoleResponse'][i]}`;
              terminal2.appendChild(output);
            }
            terminal1.parentElement.scrollTop = terminal1.parentElement.scrollHeight;
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

// Get Simcraft Commands
function fetchcommands(){
  $.ajax({
      // fo/views.fetchcommands
      url: 'fetchcommands',
      type: 'GET',
      dataType: 'json',

      success: (data) => {
          for (var i = 0; i < data['commands'].length; i++) {
            const output = document.createElement('p');
            output.textContent = `${data['commands'][i]}`;
            terminal1.appendChild(output);
          }
          terminal1.parentElement.scrollTop = terminal1.parentElement.scrollHeight;
      }
  });
}

// Refresh SimCraft Attributes
function fetchdata(){
    $.ajax({
        // fo/views.fetchdata
        url: 'fetchdata',
        type: 'GET',
        dataType: 'json',

        success: (data) => {
    
          if (data['input'].length > terminal2.children.length){
            terminal2.replaceChildren();
            for (var i = 0; i < data['input'].length; i++) {
              const output = document.createElement('p');
              output.textContent = `$ ${data['input'][i]}`;
              terminal2.appendChild(output);
            }
            terminal2.parentElement.scrollTop = terminal2.parentElement.scrollHeight;
          }
        }
    });
}

// Set Refresh Rate
$(document).ready(function(){
    setInterval(fetchdata,5000);
});