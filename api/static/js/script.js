options = [
  {
    label: "Buscas",
    value:
      "A ação de procurar, investigar ou examinar com autorização legal, em busca de evidências ou informações relevantes para uma investigação ou processo legal.",
  },
  {
    label: "Prescrição",
    value:
      "A perda do direito de punir ou de exigir o cumprimento de uma obrigação legal devido ao decurso de determinado prazo estabelecido por lei.",
  },
  {
    label: "Fraude Fiscal",
    value:
      "A prática intencional de enganar as autoridades fiscais por meio de manipulação ou ocultação de informações financeiras, com o objetivo de evitar o pagamento de impostos devidos.",
  },
  {
    label: "Arguido",
    value:
      "Indivíduo que está sob investigação ou acusação formal de um crime, ainda sem uma sentença definitiva emitida pelo tribunal.",
  },
  {
    label: "Corrupção",
    value:
      "Desvio ilícito de poder ou recursos para obtenção de vantagens indevidas ou prejuízo ao interesse público.",
  },
  {
    label: "Branqueamento de Capitais",
    value:
      "A ação de ocultar ou dissimular a origem ilegal de dinheiro ou bens obtidos de atividades criminosas, fazendo com que eles aparentem ter uma origem legítima.",
  },
];

options_en = [
  {
    label: "Search",
    value:
      'to examine another\'s premises (including a vehicle) to look for evidence of criminal activity. It is unconstitutional under the 4th and 14th Amendments for law enforcement officers to conduct a search without a "search warrant" issued by a judge or without facts which give the officer "probable cause" to believe evidence of a specific crime is on the premises and there is not enough time to obtain a search warrant.',
  },
  {
    label: "Statute of Limitations",
    value:
      "a law which sets the maximum period which one can wait before filing a lawsuit, depending on the type of case or claim. The periods vary by state. Federal statutes set the limitations for suits filed in federal courts. If the lawsuit or claim is not filed before the statutory deadline, the right to sue or make a claim is forever dead (barred).",
  },
  {
    label: "Evasion of Tax",
    value:
      'the intentional attempt to avoid paying taxes through fraudulent means, as distinguished from late payment, using legal "loopholes" or errors.',
  },
  {
    label: "Defendant",
    value:
      "the party sued in a civil lawsuit or the party charged with a crime in a criminal prosecution. In some types of cases (such as divorce) a defendant may be called a respondent.",
  },
  {
    label: "Corruption",
    value:
      "the illegal and unethical act of using one's position of power or influence for personal gain or to obtain unlawful advantages, typically involving bribery, embezzlement, or abuse of public office, and resulting in the distortion of public trust, undermining fair and transparent governance, and compromising the integrity of institutions and processes. (ChatGPT definition)",
  },
  {
    label: "Money Laundering",
    value:
      "the process of concealing the origins of illegally obtained funds or assets by making them appear legitimate, typically involving complex transactions, layering of financial activities, and integration into the legitimate economy, with the aim of disguising the illicit nature of the funds and enabling their use without detection or suspicion of illegal activity. (ChatGPT definition)",
  },
];

options.sort((a, b) => (a.label > b.label ? 1 : b.label > a.label ? -1 : 0));

options_en.sort((a, b) => (a.label > b.label ? 1 : b.label > a.label ? -1 : 0));

dictionary = [];

tinymce.init({
  selector: "#notepad",
  skin: "naked",
  //icons: "small",
  menubar: false,
  branding: false,
  elementpath: false,
  //resize: false,
  //statusbar: false,
  height: 375,
  min_heigh: 375,
  max_height: 650,
  //powerpaste linkchecker export
  plugins:
    "preview autolink directionality fullscreen media template codesample table pagebreak nonbreaking insertdatetime advlist lists help",
  toolbar:
    "export undo redo | fontfamily fontsize | bold italic underline | alignleft aligncenter alignright alignjustify",
  content_css: "../static/css/notepad.css",
  setup: function (editor) {
    editor.on("LoadContent", function (e) {
      let notes = sessionStorage.getItem("notepad");
      console.log(notes);
      tinymce.activeEditor.setContent(notes);
    });
  },
});

let selector = document.querySelector("#multipleSelect");
let notepad = document.getElementById("notepad");
let peopleBtn = document.getElementById("people");
let companiesBtn = document.getElementById("companies");
let specificsBtn = document.getElementById("specifics");
let generalBtn = document.getElementById("general");
let summaryBtn = document.getElementById("summary");
let keyWordDiv = document.getElementById("keyworddiv");
let dictDiv = document.getElementById("legal-dictionary");
let categoryDiv = document.getElementById("category-list");
let homeBtn = document.getElementById("home-button");
let keepBtn = document.getElementById("keep");

selector.setOptions(options);

selector.addEventListener("beforeClose", function () {
  let selectedData = selector.getSelectedOptions();

  updateSpan(selectedData);
});

selector.addEventListener("reset", function () {
  let selectedData = selector.getSelectedOptions();

  updateSpan(selectedData);
});

function updateSpan(selectedData) {
  keyWordDiv.innerHTML = "";
  dict = [];
  for (let i = 0; i < selectedData.length; i++) {
    let newSpan = document.createElement("span");
    newSpan.classList.add("key-word");
    newSpan.textContent = selectedData[i].label;
    keyWordDiv.appendChild(newSpan);
    dict.push({
      term: selectedData[i].label,
      definition: selectedData[i].value,
    });
  }
  addDictionaryEntry(dict);

  let tmp = dict.map((a) => a.term.toLowerCase());

  for (let i = 0; i < tmp.length; i++) {
    tmp[i] = tmp[i].replaceAll(" ", "-");
    dictionary.push(tmp[i]);
  }
}

function addDictionaryEntry(dict) {
  let ul = document.createElement("ul");
  ul.classList.add("ul-dict");
  dictDiv.appendChild(ul);
  for (let i = 0; i < dict.length; i++) {
    let div = document.createElement("div");
    div.classList.add("dict-div");
    ul.appendChild(div);
    let li = document.createElement("li");
    div.appendChild(li);
    let p = document.createElement("p");
    p.classList.add("dict-item");
    li.appendChild(p);
    p.innerHTML = "<b>" + dict[i].term + ": </b>" + dict[i].definition;
    let btn = document.createElement("button");
    term = dict[i].term.toLowerCase();
    term = term.replaceAll(" ", "-");
    p.setAttribute("id", term);
    btn.setAttribute("id", "btn-" + term);
    btn.setAttribute("title", "Add to notepad");
    btn.classList.add("keep-btn");
    btn.innerHTML = "Guardar";
    btn.addEventListener("click", function () {
      addNote(p.innerHTML);
    });
    div.appendChild(btn);
  }
}

function downloadNotes() {
  let notes = tinymce.get("notepad").getContent();
  var opt = {
    margin: 1,
    filename: "notes.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
  };
  html2pdf().set(opt).from(notes).save();

  /*
  const file = new File([notes], "notes.txt", {
    type: "text/plain;charset=utf-8",
  })

  const link = document.createElement("a");
  const url = URL.createObjectURL(file);

  link.href = url;
  link.download = file.name;
  document.body.appendChild(link);
  link.click();

  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
  */
}

function addNote(text) {
  //text1 = text.replace("<b>", "");
  //text2 = text1.replace("</b>", "");
  //notepad.textContent += "\r\n" + text2 + "\r\n";
  let notepad = tinymce.get("notepad").getContent();
  tinymce.get("notepad").setContent(notepad + text);
}

if (keepBtn) {
  keepBtn.addEventListener("click", function () {
    let ctxSummary = document.getElementById("ctxsummary").innerText;
    let notepad = tinymce.get("notepad").getContent();
    tinymce.get("notepad").setContent(notepad + ctxSummary);
  });
}

function pageReloaded() {
  let pageAccessedByReload = window.performance
    .getEntriesByType("navigation")
    .map((nav) => nav.type)
    .includes("reload");

  return pageAccessedByReload;
}

let tmpButtonValue = "";

let clicked = false;
homeBtn.addEventListener("click", function () {
  clicked = true;
});

window.onload = function () {
  //et notes = sessionStorage.getItem("notepad");
  //console.log(notes);
  //tinymce.activeEditor.setContent(notes);

  let definitions = sessionStorage.getItem("dictionaryDiv");
  if (definitions !== null) dictDiv.innerHTML = definitions;

  //let keywords = sessionStorage.getItem("keywords");
  //if (keywords !== null) keyWordDiv.innerHTML = keywords;

  //let select = sessionStorage.getItem("select");
  //if (select !== null) selector = select;

  tmpButtonValue = sessionStorage.getItem("tmpBtnValue");
  if (tmpButtonValue == sessionStorage.getItem("checkedBtn")) {
    let ctgResults = sessionStorage.getItem("categoryDiv");
    if (ctgResults !== null) categoryDiv.innerHTML = ctgResults;
  }

  let dict = JSON.parse(sessionStorage.getItem("dict"));
  if (dict !== null) dictionary = dict;

  texts = [];
  buttons = [];

  for (let i = 0; i < dictionary.length; i++) {
    p = document.getElementById(dictionary[i]);
    btn = document.getElementById("btn-" + dictionary[i]);
    texts.push(p.innerHTML);
    buttons.push(btn);
  }

  buttons.forEach(function (button, i) {
    button.addEventListener("click", function () {
      addNote(texts[i]);
    });
  });

  let radioBtnChecked = sessionStorage.getItem("checkedBtn");
  if (radioBtnChecked == peopleBtn.value) peopleBtn.checked = true;
  if (radioBtnChecked == companiesBtn.value) companiesBtn.checked = true;
  if (radioBtnChecked == specificsBtn.value) specificsBtn.checked = true;
  if (radioBtnChecked == generalBtn.value) generalBtn.checked = true;
  if (radioBtnChecked == summaryBtn.value) summaryBtn.checked = true;
};

window.onbeforeunload = function () {
  if (!clicked) {
    sessionStorage.setItem("dictionaryDiv", dictDiv.innerHTML);
  } else {
    sessionStorage.setItem("notepad", "");
    sessionStorage.setItem("dictionaryDiv", "");
  }
  sessionStorage.setItem("dict", JSON.stringify(dictionary));
  let notepad = tinymce.activeEditor.getContent();
  console.log(notepad);
  sessionStorage.setItem("notepad", notepad);
  //sessionStorage.setItem("keywords", keyWordDiv.innerHTML);
  //sessionStorage.setItem("select", selector);

  tmpButtonValue = sessionStorage.getItem("checkedBtn");
  sessionStorage.setItem("tmpBtnValue", tmpButtonValue);

  if (peopleBtn.checked) sessionStorage.setItem("checkedBtn", peopleBtn.value);
  if (companiesBtn.checked)
    sessionStorage.setItem("checkedBtn", companiesBtn.value);
  if (specificsBtn.checked)
    sessionStorage.setItem("checkedBtn", specificsBtn.value);
  if (generalBtn.checked)
    sessionStorage.setItem("checkedBtn", generalBtn.value);
  if (summaryBtn.checked)
    sessionStorage.setItem("checkedBtn", summaryBtn.value);

  if (!clicked) {
    if (categoryDiv.innerHTML.includes("table")) {
      sessionStorage.setItem("categoryDiv", categoryDiv.innerHTML);
    }
  } else {
    sessionStorage.setItem("categoryDiv", "");
  }
};
