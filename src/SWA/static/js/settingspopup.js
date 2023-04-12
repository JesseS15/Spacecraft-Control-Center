//get modals
var modal1 = document.getElementById("modal1");

//get buttons
const btns = document.getElementsByClassName("settings"); 
var myDiv = document.getElementById("test");
//var class_name = document.getElementById()
//var btn = document.getElementById(class_name);
const btnname = [];
//const classes = "{{classes|escapejs}}"
//btn.onclick = function(){
  //  window.alert()
//}

//get span
var span1 = document.getElementById("span1");

/*function changeClass(class_name){
    var btn = document.getElementById(class_name);
    alert(btn);
}*/

for(i=0; i<btns.length; i++){
    btnname[i] = btns[i].id 
}

for(let i=0; i<btns.length; i++){
    btns[i].onclick = function() {
        var test1 = btns[i].id;
        document.getElementById("myInput").value = test1;
        //document.getElementById("test").innerHTML = '';
        if(modal2.style.display == "none" && modal3.style.display =="none"){
            var myDiv = document.getElementById("test").innerHTML = "Edit " + btns[i].id;
            $('#modal1').show();
        }else{
            $('#modal2').hide();
            $('#modal3').hide();
            var myDiv = document.getElementById("test").innerHTML = "Edit " + btns[i].id;
            $('#modal1').show(); 
        }
        
        //document.getElementById("test").innerHTML = '';
    }  
}
/*btns.addEventListener
    btns[i].addEventListener("click", function(event){
        if(modal2.style.display == "none" && modal3.style.display =="none"){
            var myDiv = document.getElementById("test").innerHTML = "Edittt " + btns[i].id;
            $('#modal1').show();
        }else{
            $('#modal2').hide();
            $('#modal3').hide();
            var myDiv = document.getElementById("test").innerHTML = "Edit " + btns[i].id;
            $('#modal1').show(); 
        }
    });
}*/


span1.onclick = function(){
    //document.getElementById("test").innerHTML = '';
    $('#modal1').hide();
}

window.addEventListener("click", function(event){
    if(event.target == modal1){
        //document.getElementById("test").innerHTML = '';
        modal1.style.display = "none";
    }else{
        modal1.style.position = "fixed";
        modal1.style.zIndex = "2";
        modal1.style.margin = "auto auto";
        modal1.style.width = ""; 

    }
});