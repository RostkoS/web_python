document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById('hi').classList.toggle('.act');
   setInterval(ch, 3000);
});
function ch()
{

    var t = document.getElementById('hi').classList;
    if(t=="text .act"){
document.getElementById('hi').classList.toggle('.act');
document.getElementById('hi').style.opacity = 0;

    document.getElementById('hello').classList.toggle('.act');
    document.getElementById('hello').style.opacity=1;
    //window.alert(t);
    }
    else{  
        document.getElementById('hello').classList.toggle('.act');
        document.getElementById('hello').style.opacity = 0;
            document.getElementById('hi').classList.toggle('.act');
            document.getElementById('hi').style.opacity=1;
    }
}

let elem = document.getElementById('exampleModal')
let modal = new Modal(elem)
modal.show()

