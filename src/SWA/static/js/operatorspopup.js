//get modals
var modal5 = document.getElementById("modal5");

//get buttons
const opbtns = document.getElementsByClassName("op"); 

//get span
var span3 = document.getElementById("span5");


for(i=0; i<opbtns.length; i++){
    opbtns[i].onclick = function() {
        if(modal4.style.display == "none" && modal5.style.display == "none"){
            $('#modal5').show();
        }else{
            $('#modal5').hide();
            $('#modal4').hide(); 
            $('#modal4').show();
        }
    }
}

span3.onclick = function(){
    $('#modal5').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal3){
        modal5.style.display = "none";
    }else{
        modal5.style.position = "relative";
        modal5.style.zIndex = "1";
        modal5.style.margin = "auto auto";
        modal5.style.width = ""; 
    }
});