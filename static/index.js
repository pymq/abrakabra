function someFunc() {
    var textForUser;
    textForUser="Thank you :3";
    document.getElementById('rezultat').innerHTML = textForUser;
    setTimeout ("emptyText()", 1000);
}
function emptyText (){
    var textForUser;
    textForUser="";
    document.getElementById('rezultat').innerHTML = textForUser;
}
document.getElementById("btn").onclick = function () { someFunc();};