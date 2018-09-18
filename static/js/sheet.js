// email
function School_Email() {
    var email = "";
    let item = document.getElementsByClassName("SID");
    for (var i = 0; i < item.length; i++) {
        email += 's' + item[i].innerHTML.trim() + "@mail1.ncnu.edu.tw, ";
    }
    email = email.substr(0, email.length - 2);
    console.log(email);
    document.getElementById("ShowEmail").innerHTML =
    '<input onmouseover="this.select()" value="' +
    email +
    '" />' +
    " &nbsp;<b>滑鼠移到上面複製即可</b>";
}
function Primary_Email() {
    var email = "";
    let item = document.getElementsByClassName("EMAIL");
    for (var i = 0; i < item.length; i++) {
        if (item[i].innerHTML.trim() != ''){
            email += item[i].innerHTML.trim() + ", ";
        }
    }
    console.log(email);
    email = email.substr(0, email.length - 2);
    document.getElementById("ShowEmail").innerHTML =
        '<input onmouseover="this.select()" value="' +
        email +
        '" />' +
        " &nbsp;<b>滑鼠移到上面複製即可</b>";
}

// export excel
$("#export").click(function() {
  $("table").tableToCSV();
});

$("table").tablesorter();
