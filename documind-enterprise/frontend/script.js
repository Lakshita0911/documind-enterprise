
/* Upload PDF */

async function uploadPDF() {

    const fileInput =
        document.getElementById("pdfFile");

    const file = fileInput.files[0];

    if (!file) {

        alert("Select a PDF first");

        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    // Show Loading

    document.getElementById("loading")
        .style.display = "block";

    try{

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        if(!response.ok){

            throw new Error("Upload failed");

        }

        const result = await response.json();

        // Upload Success

        document.getElementById("uploadStatus")
            .innerHTML =
            `✅ Uploaded Successfully 
             (${result.chunks} chunks)`;

    }

    catch(error){

        alert("Error uploading PDF");

        console.log(error);

    }

    finally{

        document.getElementById("loading")
            .style.display = "none";

    }

}


/* Chat History */

let historyHTML = "";


/* Ask Question */

async function askQuestion() {

    const question =
        document.getElementById("question").value;

    if (!question) {

        alert("Enter question");

        return;
    }

    // Show Loading

    document.getElementById("loading")
        .style.display = "block";

    try{

        const response = await fetch(
            `http://127.0.0.1:8000/ask?query=${encodeURIComponent(question)}`
        );

        if(!response.ok){

            throw new Error("Server Error");

        }

        const result = await response.json();

        // Chat History

        historyHTML += `

            <div class="chat-card">

                <div class="user-msg">

                    <strong>🧑 You:</strong>

                    <p>${question}</p>

                </div>

                <div class="ai-msg">

                    <strong>🤖 AI:</strong>

                    <p>${result.answer}</p>

                </div>

            </div>

        `;

        document.getElementById("chatHistory")
            .innerHTML = historyHTML;

        // Auto Scroll

        document.getElementById("chatHistory")
            .scrollTop =

        document.getElementById("chatHistory")
            .scrollHeight;

        // Main Answer

        document.getElementById("answerText")
            .innerText = result.answer;

        // Source Cards

        let sourceHTML = "";

        result.sources.forEach(src => {

            sourceHTML += `

                <div class="source-card">

                    <h4>📄 ${src.source}</h4>

                    <p>Page: ${src.page+1}</p>

                </div>

            `;

        });

        document.getElementById("sourceText")
            .innerHTML = sourceHTML;

        // Clear Input

        document.getElementById("question").value = "";

    }

    catch(error){

        alert("Error getting answer");

        console.log(error);

    }

    finally{

        // Hide Loading

        document.getElementById("loading")
            .style.display = "none";

    }

}


/* Summarize PDF */

async function summarizePDF() {

    document.getElementById("loading")
        .style.display = "block";

    try{

        const response = await fetch(
            "http://127.0.0.1:8000/ask?query=Summarize%20this%20document"
        );

        const result = await response.json();

        document.getElementById("answerText")
            .innerText = result.answer;

    }

    catch(error){

        alert("Error generating summary");

        console.log(error);

    }

    finally{

        document.getElementById("loading")
            .style.display = "none";

    }

}


/* Enter Key Support */

document.getElementById("question")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        askQuestion();

    }

});


/* Theme Toggle */

function toggleTheme(){

    document.body.classList.toggle("light-mode");

    const btn =
        document.getElementById("themeBtn");

    if(document.body.classList.contains("light-mode")){

        btn.innerHTML = "☀️";

    }
    else{

        btn.innerHTML = "🌙";

    }

}
