function generateInputFields() {
  const count = parseInt(document.getElementById("coCount").value);
  const container = document.getElementById("inputFields");
  container.innerHTML = "";
  if (isNaN(count) || count <= 0) return alert("Enter a valid number of COs.");

  for (let i = 0; i < count; i++) {
    container.innerHTML += `
      <label>CO${i + 1}:</label>
      <textarea placeholder="Enter CO${i + 1} statement"></textarea>
    `;
  }
}

async function generateCAM() {
  const inputs = document.querySelectorAll("#inputFields textarea");
  const coTexts = Array.from(inputs).map(x => x.value.trim());
  const subject = document.getElementById("subjectInput").value.trim();

  if (!subject) return alert("Please enter the subject name.");
  if (coTexts.some(t => t === "")) return alert("All COs must be filled.");

  const res = await fetch("/api/rate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ set_i: coTexts })
  });

  const data = await res.json();
  buildTable(data, coTexts.length, subject);
}

function buildTable(data, coCount, subject) {
  let html = `<h3>Subject: ${subject}</h3>`;
  html += `<table><tr><th rowspan="2">COs</th><th colspan="12">POs</th><th colspan="2">PSOs</th></tr><tr>`;
  for (let i = 1; i <= 12; i++) html += `<th>${i}</th>`;
  html += `<th>1</th><th>2</th></tr>`;

  for (let i = 0; i < coCount; i++) {
    html += `<tr><td>CO${i + 1}</td>`;
    for (let j = 0; j < data.length; j++) {
      const val = data[j][`SET_I_${i + 1}`];
      if (val === 0) {
        html += `<td class="score-0">-</td>`;
      } else {
        html += `<td class="score-${val}">${val}</td>`;
      }
    }
    html += `</tr>`;
  }

  html += `</table>`;
  document.getElementById("outputTable").innerHTML = html;
}

function downloadCSV() {
  const table = document.querySelector("#outputTable table");
  if (!table) return alert("Generate the matrix first.");
  let csv = [];

  for (let row of table.rows) {
    let line = [];
    for (let cell of row.cells) {
      line.push(cell.innerText.replace(/,/g, " "));
    }
    csv.push(line.join(","));
  }

  const blob = new Blob([csv.join("\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "CAM_matrix.csv";
  a.click();
}

function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
}
