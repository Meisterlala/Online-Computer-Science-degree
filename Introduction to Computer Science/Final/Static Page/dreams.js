let pricelist = [
  [2.5, "Coffees"],
  [20.37, "Servings in a restaurant"],
  [27, "Copys of Minecraft"],
  [60, "AAA Games"],
  [300, "PS4s"],
  [1000, "Gaming PCs"],
  [34000, "Cars"],
];

function RefreshList() {
  let c = localStorage.getItem("history");
  if (!c) {
    return;
  }

  let h = JSON.parse(c);

  let total = h.length * 2.5;

  $("#moneyy").html(
    "You wasted " +
      total +
      "$ on " +
      h.length +
      " Keys<br>" +
      "You could have bought:"
  );

  let towrite = "";
  for (i = 0; i < pricelist.length; i++) {
    towrite = towrite.concat('<tr><td class="text-right">');
    towrite = towrite.concat(Math.floor(total / pricelist[i][0]));
    towrite = towrite.concat("</td><td>");
    towrite = towrite.concat(pricelist[i][1]);
    towrite = towrite.concat("</td></tr>");
  }

  $("#dreamTable").html(towrite);
}

$(document).ready(function () {
  RefreshList();
});
