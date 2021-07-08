


//
// function tg(t){
//     t.fontWeight=t.fontWeight=="bold"?"normal":"bold";
//     t.textDecoration =t.textDecoration =="none"?"underline ":"none";
//
// }


function clickLi(Pelement) {

    var nestedList = Pelement.childNodes[1];

    Pelement.style.fontWeight=Pelement.style.fontWeight=="bold"?"normal":"bold";
    Pelement.style.textDecoration =Pelement.style.textDecoration =="none"?"underline":"none";

    if (nestedList.classList) {
        nestedList.classList.toggle("not-clicked");


    } else {
        var classes = nestedList.className.split(" ");
        var i = classes.indexOf("not-clicked");

        if (i >= 0)
            classes.splice(i, 1);
        else
            classes.push("not-clicked");
        nestedList.className = classes.join(" ");
    }
}


//
// $(document).ready(function () {
//     $("#nesting-list li").click(function () {
//         $("nesting-list li").removeClass('clicked');
//         $(this).addClass('clicked');
//     });
// });

// $(document).ready(function () {
//     $("#list3 li").click(function () {
//         $("#list3 li").removeClass('clicked');
//         $(this).addClass('clicked');
//
//     });
// });
