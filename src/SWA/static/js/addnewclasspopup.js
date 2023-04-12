//get modals
var modal2= document.getElementById("modal2");
//get buttons
var btn1 = document.getElementById("addclass");

//get spans
var span2 = document.getElementById("span2");

btn1.onclick = function(){
    if(modal1.style.display == "none" && modal3.style.display == "none"){
        $('#modal2').show();
    }else{
        $('#modal1').hide(); 
        $('#modal3').hide(); 
        $('#modal2').show(); 
    }
}

span2.onclick = function(){
    $('#modal2').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal2){
        modal2.style.display = "none";
    }else{
        modal2.style.position = "fixed";
        modal2.style.zIndex = "2";
        modal2.style.margin = "auto auto";
        modal2.style.width = ""; 
    }
});