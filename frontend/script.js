async function askQuestion() {

    const questionInput = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");
    const askButton = document.getElementById("ask-button");

    const question = questionInput.value.trim();

    // Don't send empty questions
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

    // Clear input
    questionInput.value = "";

    // Disable button while processing
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

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("http://127.0.0.1:8000/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("Backend request failed");
        }

        const data = await response.json();

        // Remove loading message
        loadingMessage.remove();

        // Display AI answer
        const botMessage = document.createElement("div");

        botMessage.className = "message bot-message";

        botMessage.innerHTML = `
            <div class="avatar">🤖</div>

            <div class="message-content">
                <strong>ExamPrep AI</strong>
                <p>${formatAnswer(data.answer)}</p>
            </div>
        `;

        chatBox.appendChild(botMessage);

    } catch (error) {

        loadingMessage.remove();

        const errorMessage = document.createElement("div");

        errorMessage.className = "message bot-message";

        errorMessage.innerHTML = `
            <div class="avatar">⚠️</div>

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


// Convert new lines into HTML line breaks
function formatAnswer(answer) {

    return escapeHtml(answer)
        .replace(/\n/g, "<br>");
}


// Prevent HTML injection from user input
function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// Allow pressing Enter to send the question
document.getElementById("question").addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        askQuestion();
    }

});