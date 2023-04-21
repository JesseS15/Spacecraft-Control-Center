var modal4 = document.getElementById("modal4");
//get buttons
const dbtns = document.getElementsByClassName("download"); 
const ebtns = document.getElementsByClassName("edit"); 

var span4 = document.getElementById("span4");

for(let i=0; i<ebtns.length; i++){
    ebtns[i].onclick = function() {
        var test1 = ebtns[i].id
        document.getElementById("myInput").value = test1;
        //document.getElementById("test").innerHTML = '';
        var myDiv = document.getElementById("test").innerHTML = "Edit " + ebtns[i].id;
        $('#modal4').show();

        //document.getElementById("test").innerHTML = '';
    }  
}
span4.onclick = function(){
    //document.getElementById("test").innerHTML = '';
    $('#modal4').hide();
}


window.addEventListener("click", function(event){
    if(event.target == modal4){
        //document.getElementById("test").innerHTML = '';
        modal4.style.display = "none";
        $('#modal4').hide();
    }else{
        modal4.style.position ="fixed";
        modal4.style.zIndex = "1";
        modal4.style.margin = "auto auto";
        modal4.style.width = ""; 
    }
});

for(let i=0; i<dbtns.length; i++){
    dbtns[i].onclick = function() {
        $.ajax({
              // tc/views.downloadSimReport
              url: 'downloadSimReport/',
              type: 'GET',
              dataType: 'json',
              
              data:{
                simkey : String(dbtns[i].id),
              },
  
              success: function( data )
              {
                const link = document.createElement("a");
                const file = new Blob([data['report']], {type: 'text/plain' });
                link.href = URL.createObjectURL(file);
                link.download = data['sim_name']+'_Report.doc';
                link.click();
                URL.revokeObjectURL(link.href);
              }
         })
    }
}
