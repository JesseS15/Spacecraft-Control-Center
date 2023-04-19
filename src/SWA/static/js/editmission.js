var modal5 = document.getElementById("modal5");
//get buttons 
const btns = document.getElementsByClassName("missionedit"); 

var span4 = document.getElementById("span5");

for(let i=0; i<btns.length; i++){
    btns[i].onclick = function() {
        var test1 = btns[i].id;
        document.getElementById("missionname").value = test1;
        //document.getElementById("test").innerHTML = '';
        var difvar = document.getElementById("editmissionheader").innerHTML = "Edit " + btns[i].id;
        if(modal5.style.display == "none"){
            $('#modal5').show();
        }else{
            $('#modal4').hide(); 
            $('#modal5').show(); 
        }
        //document.getElementById("test").innerHTML = '';
    }  
}
span4.onclick = function(){
    //document.getElementById("test").innerHTML = '';
    $('#modal5').hide();
}


window.addEventListener("click", function(event){
    if(event.target == modal5){
        //document.getElementById("test").innerHTML = '';
        modal5.style.display = "none";
    }else{
        modal5.style.position ="fixed";
        modal5.style.zIndex = "1";
        modal5.style.margin = "auto auto";
        modal5.style.width = ""; 
    }
});
