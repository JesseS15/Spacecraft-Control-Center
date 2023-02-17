//get modals
var modal= document.getElementById("modal4");
//get buttons
var btn4 = document.getElementById("addsim");

//get spans
var span4 = document.getElementById("span4");

btn4.onclick = function(){
    $('#modal4').show();
}

span4.onclick = function(){
    $('#modal4').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal4){
        modal4.style.display = "none";
    }else{
        modal4.style.position = "relative";
        modal4.style.zIndex = "1";
        modal4.style.margin = "auto auto";
        modal4.style.width = ""; 
    }
});