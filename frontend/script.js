const API = "http://127.0.0.1:8000";

console.log("JS LOADED");

// UPLOAD
async function uploadFiles() {
    let files = document.getElementById("files").files;

    if (files.length === 0) {
        alert("Select files first");
        return;
    }

    let formData = new FormData();

    for (let f of files) {
        formData.append("files", f);
    }

    try {
        let res = await fetch(`${API}/upload`, {
            method: "POST",
            body: formData
        });

        let data = await res.json();

        alert("✅ Upload successful");
        console.log(data);

    } catch (err) {
        console.error(err);
        alert("❌ Upload failed");
    }
}

// ASK
async function askQuestion() {
    let queryInput = document.getElementById("query");
    let query = queryInput.value;

    if (!query) return;

    let formData = new FormData();
    formData.append("query", query);

    try {
        let res = await fetch(`${API}/ask`, {
            method: "POST",
            body: formData
        });

        let data = await res.json();

        let chat = document.getElementById("chat");

        // 🔥 FIX 1: preserve line breaks
        let formattedAnswer = data.answer.replace(/\n/g, "<br>");

        chat.innerHTML += `
            <div class="user">You: ${query}</div>
            <div class="bot">Bot: ${formattedAnswer}</div>
            <div class="source">Sources: ${data.sources.join(", ")}</div>
            <hr>
        `;

        // 🔥 FIX 2: clear input
        queryInput.value = "";

        chat.scrollTop = chat.scrollHeight;

    } catch (err) {
        console.error(err);
        alert("❌ Request failed");
    }
}