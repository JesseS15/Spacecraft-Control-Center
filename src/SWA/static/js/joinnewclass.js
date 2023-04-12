//get modals
var modal1= document.getElementById("modal1");
//get buttons
var btn1 = document.getElementById("joinclass");

//get spans
var span2 = document.getElementById("span1");


btn1.onclick = function(){
    $('#modal1').show();
}

span1.onclick = function(){
    $('#modal1').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal1){
        modal1.style.display = "none";
    }else{
        modal1.style.position = "fixed";
        modal1.style.zIndex = "1";
        modal1.style.margin = "auto auto";
        modal1.style.width = ""; 
    }
});