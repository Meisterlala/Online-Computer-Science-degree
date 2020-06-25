console.log("Hello workld");


let currentCaseName;

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function RefreshList() {
  let c = getCookie("history");
  if (c == "") {
    return;
  }
  let h = JSON.parse(c);
  let towrite = "";

  for (i = h.length - 1; i > 0; i--) {
    towrite = towrite.concat("<tr><td>");
    towrite = towrite.concat(h[i][0]);
    towrite = towrite.concat('</td><td><span style="color:');
    towrite = towrite.concat(h[i][1]);
    towrite = towrite.concat('">');
    towrite = towrite.concat(h[i][2]);
    towrite = towrite.concat("</span></td></tr>");
  }

  $("#tableHistory").html(towrite);
}

function GetSelected() {
  $("dropDownCase").dropdown();
}

function Open() {
  if (!currentCaseName) {
    return;
  }
  // chose random
  let selectedCase;
  cases.forEach((element) => {
    if (element[0] == currentCaseName) {
      selectedCase = element;
    }
  });

  if (!selectedCase) {
    console.log("Could not find: " + currentCaseName + " in data");
    return;
  }

  let rarity;
  let r = Math.random();
  if (r <= 0.8) {
    rarity = "blue";
  } else if (0.8 < r <= 0.93) {
    rarity = "purple";
  } else if (0.93 < r <= 0.98) {
    rarity = "pink";
  } else {
    rarity = "red";
  }

  let selectedGroup = selectedCase[1][rarity];
  let r2 = Math.floor(Math.random() * (selectedGroup.length - 1)) + 1;
  let drop = selectedGroup[r2];

  console.log(currentCaseName + ", " + rarity + ", " + drop);

  let h;
  // add to cookie
  let c = getCookie("history");
  if (c == "") {
    h = [];
  } else {
    h = JSON.parse(c);
  }

  h.push([currentCaseName, rarity, drop]);
  setCookie("history", JSON.stringify(h));

  RefreshList();
}

function LoadDropdown() {
  let towrite = "";
  cases.forEach((element) => {
    towrite = towrite.concat(
      '<a class="dropdown-item" role="presentation" href="#">'
    );
    towrite = towrite.concat(element[0]);
    towrite = towrite.concat("</a>");
  });

  $("#dropDownCase").html(towrite);
}

$(document).ready(function () {
  // Open Case
  $("#openB").click(function () {
    Open();
  });

  // Open Dropbox
  LoadDropdown();
  $("#dropDownCase a").on("click", function () {
    let name = $(this).text();
    console.log("Selected: " + name);
    $("#dropdownCaseButton").text(name);
    currentCaseName = name;
  });

  // Initilize Cookie
  if (!getCookie("history")) {
    setCookie("history", "");
  }

  // Load from cookie
  RefreshList();
});
