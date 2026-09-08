async function askQuestion() {

    const questionInput = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");
    const askButton = document.getElementById("ask-button");

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    // Display user's question
    const userMessage = document.createElement("div");

    userMessage.className = "message user-message";

    userMessage.innerHTML = `
        <div class="message-content">
            <strong>You</strong>
            <p>${escapeHtml(question)}</p>
        </div>

        <div class="avatar">👤</div>
    `;

    chatBox.appendChild(userMessage);

    questionInput.value = "";

    // Disable buttons while processing
    askButton.disabled = true;
    askButton.textContent = "Thinking...";


    // Loading message
    const loadingMessage = document.createElement("div");

    loadingMessage.className = "message bot-message";

    loadingMessage.innerHTML = `
        <div class="avatar">🤖</div>

        <div class="message-content">
            <strong>ExamPrep AI</strong>
            <p>Thinking... ⏳</p>
        </div>
    `;

    chatBox.appendChild(loadingMessage);

    chatBox.scrollTop = chatBox.scrollHeight;


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        if (!response.ok) {
            throw new Error("Backend request failed");
        }


        const data = await response.json();


        // Remove loading message
        loadingMessage.remove();


        // Create sources section
        let sourcesHTML = "";

        if (data.sources && data.sources.length > 0) {

            sourcesHTML = `
                <div class="sources">

                    <strong>📚 Sources</strong>

                    <ul>
                        ${data.sources.map(
                            source => `<li>${escapeHtml(source)}</li>`
                        ).join("")}
                    </ul>

                </div>
            `;
        }


        // Display AI answer
        const botMessage = document.createElement("div");

        botMessage.className = "message bot-message";

        botMessage.innerHTML = `

            <div class="avatar">
                🤖
            </div>

            <div class="message-content">

                <strong>ExamPrep AI</strong>

                <div class="answer">
                    ${formatAnswer(data.answer)}
                </div>

                ${sourcesHTML}

            </div>

        `;

        chatBox.appendChild(botMessage);


    } catch (error) {

        loadingMessage.remove();


        const errorMessage = document.createElement("div");

        errorMessage.className = "message bot-message";

        errorMessage.innerHTML = `

            <div class="avatar">
                ⚠️
            </div>

            <div class="message-content">

                <strong>Error</strong>

                <p>
                    Unable to connect to the ExamPrep AI backend.
                    Please make sure the FastAPI server is running.
                </p>

            </div>

        `;

        chatBox.appendChild(errorMessage);

        console.error(error);

    } finally {

        askButton.disabled = false;
        askButton.textContent = "Send";

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}



// Clear the entire conversation
function clearChat() {

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML = `

        <div class="message bot-message">

            <div class="avatar">
                🤖
            </div>

            <div class="message-content">

                <strong>ExamPrep AI</strong>

                <p>
                    Hello! 👋 Ask me any question from your study material
                    and I'll help you prepare for your exams.
                </p>

            </div>

        </div>

    `;

    // Clear input field
    document.getElementById("question").value = "";

}



// Format AI answer
function formatAnswer(answer) {

    let formatted = escapeHtml(answer);


    // Bold text: **text**
    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    // Bullet points
    formatted = formatted.replace(
        /^- (.*)$/gm,
        "• $1"
    );


    // Numbered points
    formatted = formatted.replace(
        /^(\d+)\. (.*)$/gm,
        "<strong>$1.</strong> $2"
    );


    // New lines
    formatted = formatted.replace(/\n/g, "<br>");


    return formatted;
}



// Prevent HTML injection
function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}



// Press Enter to send question
document.getElementById("question").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            askQuestion();
        }

    }
);