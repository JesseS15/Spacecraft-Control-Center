//get modals
var modal3 = document.getElementById("modal3");

//get buttons
const opbtns = document.getElementsByClassName("operators"); 

//get span
var span3 = document.getElementById("span3");


for(i=0; i<opbtns.length; i++){
    opbtns[i].onclick = function() {
        choice = document.getElementsByClassName("classlist")[0].id;
        document.getElementById("class_test").innerHTML = choice;
        
        if(modal2.style.display == "none" && modal1.style.display == "none" && modal3.style.display == "none"){
            $('#modal3').show();
        }else{
            $('#modal2').hide();
            $('#modal1').hide(); 
            $('#modal3').hide(); 
            $('#modal3').show();
        }
    }
}

span3.onclick = function(){
    $('#modal3').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal3){
        modal3.style.display = "none";
    }else{
        modal3.style.position = "relative";
        modal3.style.zIndex = "1";
        modal3.style.margin = "auto auto";
        modal3.style.width = ""; 
    }
});