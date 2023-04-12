// fosim.js
// Purpose: Refresh simcraft attributes and submit flight operator inputs on the fo sim page.

// Create resizeable terminal
const terminal1 = document.getElementById('terminal1');
const terminal2 = document.getElementById('terminal2');
const input = document.getElementById('input');

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

// Add enter key event listener to command console
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
            terminal2.innerText = '';
            for (var i = 0; i < data.length; i++) {
              const output = document.createElement('p');
              output.textContent = `${data[i]}`;
              terminal2.appendChild(output);
            }
            terminal2.parentElement.scrollTop = terminal2.parentElement.scrollHeight;
          }
        })
  }
});

// Get Simcraft Commands
function fetchcommands(){
  $.ajax({
      // fo/views.fetchcommands
      url: 'fetchcommands',
      type: 'GET',
      dataType: 'json',

      success: (data) => {
          // Display command options on left terminal
          for (var i = 0; i < data['commandOptions'].length; i++) {
            const output = document.createElement('p');
            output.textContent = `${data['commandOptions'][i]}`;
            terminal1.appendChild(output);
          }
          terminal1.parentElement.scrollTop = terminal1.parentElement.scrollHeight;

          // Display previous commands on right terminal
          for (var i = 0; i < data['previousCommands'].length; i++) {
            const output = document.createElement('p');
            output.textContent = `${data['previousCommands'][i]}`;
            terminal2.appendChild(output);
          }
          terminal2.parentElement.scrollTop = terminal2.parentElement.scrollHeight;
      }
  });
}
fetchcommands();
