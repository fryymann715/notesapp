    function openDesc(element_id) {
        var ele = document.getElementById(element_id);
        var mainele = ele.querySelectorAll("main");

        if(mainele[0].style.display == "none") {
            mainele[0].style.display = "block";
        }
        else {
            mainele[0].style.display = "none";
        }
    }