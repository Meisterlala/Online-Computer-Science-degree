const cases = [
  [
    "Prisma 2 Case",
    {
      blue: [
        "R8 Revolver | Bone Forged",
        "Negev | Prototype",
        "MP5-SD | Desert Strike",
        "Desert Eagle | Blue Ply",
        "CZ75-Auto | Distressed",
        "AWP | Capillary",
        "AUG | Tom Cat",
      ],
      purple: [
        "P2000 | Acid Etched",
        "Sawed-Off | Apocalypto",
        "SCAR-20 | Enforcer",
        "SG 553 | Darkwing",
        "SSG 08 | Fever Dream",
      ],
      pink: [
        "AK-47 | Phantom Disruptor",
        "MAC-10 | Disco Tech",
        "MAG-7 | Justice",
      ],
      red: ["M4A1-S | Player Two", "Glock-18 | Bullet Queen "],
    },
  ],

  [
    "CS20 Case",
    {
      red: ["AWP | Wildfire", "FAMAS | Commemoration"],
      pink: ["AUG | Death by Puppy", "P90 | Nostalgia", "MP9 | Hydra"],
      purple: [
        "UMP-45 | Plastique",
        "P250 | Inferno",
        "Five-SeveN | Buddy",
        "MP5-SD | Agent",
        "M249 | Aztec",
      ],
      blue: [
        "Glock-18 | Sacrifice",
        "FAMAS | Decommissioned",
        "SCAR-20 | Assault",
        "MAG-7 | Popdog",
        "MAC-10 | Classic Crate",
        "Tec-9 | Flash Out",
        "Dual Berettas | Elite 1.6",
      ],
    },
  ],

  [
    "Shattered Web Case",
    {
      red: ["AWP | Containment Breach", "MAC-10 | Stalker"],
      pink: ["SG-553 | Colony IV", "SSG 08 | Bloodshot", "Tec-9 | Decimator"],
      purple: [
        "AK-47 | Rat Rod",
        "AUG | Arctic Wolf",
        "MP7 | Neon Ply",
        "PP-Bizon | Embargo",
        "P2000 | Obsidian",
      ],
      blue: [
        "Dual Berettas | Balance",
        "G3SG1 | Black Sand",
        "M249 | Warbird",
        "MP5-SD | Acid Wash",
        "Nova | Plume",
        "R8 Revolver | Memento",
        "SCAR-20 | Torn",
      ],
    },
  ],

  [
    "Danger Zone Case",
    {
      red: ["AWP | Neo-Noir", "AK-47 | Asiimov"],
      pink: [
        "MP5-SD | Phosphor",
        "Desert Eagle | Mecha Industries",
        "UMP-45 | Momentum",
      ],
      purple: [
        "USP-S | Flashback",
        "P250 | Nevermore",
        "MAC-10 | Pipe Down",
        "Galil AR | Signal",
        "G3SG1 | Scavenger",
      ],
      blue: [
        "Tec-9 | Fubar",
        "SG 553 | Danger Close",
        "Sawed-Off | Black Sand",
        "M4A4 | Magnesium",
        "Nova | Wood Fired",
        "Glock-18 | Oxide Blaze",
        "MP9 | Modest Threat",
      ],
    },
  ],

  [
    "Clutch Case",
    {
      red: ["M4A4 | Neo-Noir", "MP7 | Bloodsport"],
      pink: ["AWP | Mortis", "AUG | Stymphalian", "USP-S | Cortex"],
      purple: [
        "Glock-18 | Moonrise",
        "MAG-7 | SWAG-7",
        "Negev | Lionfish",
        "Nova | Wild Six",
        "UMP-45 | Arctic Wolf",
      ],
      blue: [
        "Five-SeveN | Flame Test",
        "MP9 | Black Sand",
        "P2000 | Urban Hazard",
        "PP-Bizon | Night Riot",
        "R8 Revolver | Grip",
        "SG 553 | Aloha",
        "XM1014 | Oxide Blaze",
      ],
    },
  ],
];

let currentCaseName;

function RefreshList() {
  let c = localStorage.getItem("history");
  if (!c) {
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

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function Open() {
  if (!currentCaseName) {
    alert("Please select a case");
    $("#formCheck-1")[0].checked = false;
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
  let c = localStorage.getItem("history");
  if (!c) {
    h = [];
  } else {
    h = JSON.parse(c);
  }

  h.push([currentCaseName, rarity, drop]);
  localStorage["history"] = JSON.stringify(h);
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

  $("#formCheck-1").click(async function () {
    let cb = $("#formCheck-1")[0];
    while (cb.checked) {
      Open();
      await sleep(100);
    }
  });
  // Open Dropbox
  LoadDropdown();
  $("#dropDownCase a").on("click", function () {
    let name = $(this).text();
    console.log("Selected: " + name);
    $("#dropdownCaseButton").text(name);
    currentCaseName = name;
  });

  // Load from cookie
  RefreshList();
});
