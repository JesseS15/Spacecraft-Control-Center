//get modals
var modal1 = document.getElementById("modal1");

//get buttons
const btns = document.getElementsByClassName("settings"); 

//get span
var span1 = document.getElementById("span1");

for(i=0; i<btns.length; i++){
    btns[i].onclick = function() {
        if(modal2.style.display == "none" && modal3.style.display =="none"){
            $('#modal1').show();
        }else{
            $('#modal2').hide();
            $('#modal3').hide();
            $('#modal1').show(); 
        }
}
}

span1.onclick = function(){
    $('#modal1').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal1){
        modal1.style.display = "none";
    }else{
        modal1.style.position = "relative";
        modal1.style.zIndex = "1";
        modal1.style.margin = "auto auto";
        modal1.style.width = ""; 
    }
});