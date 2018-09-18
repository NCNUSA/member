// email
var email = "";
let item = document.getElementsByClassName("SID");
for (var i = 0; i < item.length; i++) {
  email += "s" + item[i].innerHTML.trim() + "@mail1.ncnu.edu.tw, ";
}
email = email.substr(0, email.length - 2);
function show() {
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
