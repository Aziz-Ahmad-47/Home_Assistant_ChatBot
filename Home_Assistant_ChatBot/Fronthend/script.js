// =====================================================
// RANDOM SUGGESTED QUESTIONS
// =====================================================

const suggestedQuestions = [

    {
        icon: "📋",
        question: "What are my pending family tasks?"
    },

    {
        icon: "⚡",
        question: "How much was the electricity bill in June?"
    },

    {
        icon: "🛒",
        question: "How much did we spend on groceries?"
    },

    {
        icon: "💰",
        question: "What were our total monthly expenses?"
    },

    {
        icon: "📅",
        question: "What family tasks are due tomorrow?"
    },

    {
        icon: "💡",
        question: "Which month had the highest electricity bill?"
    },

    {
        icon: "🧾",
        question: "Show me our recent grocery purchases."
    },

    {
        icon: "💵",
        question: "Can you make a budget for a family of four?"
    },

    {
        icon: "🏠",
        question: "What household expenses should we control?"
    },

    {
        icon: "🛍️",
        question: "What groceries do we usually buy?"
    },

    {
        icon: "📊",
        question: "Give me a summary of our household expenses."
    },

    {
        icon: "💳",
        question: "How much money do we spend on groceries each month?"
    }

];


// =====================================================
// SHOW RANDOM QUESTIONS
// =====================================================

function showRandomQuestions() {

    const container = document.getElementById("suggestions");

    if (!container) {
        return;
    }


    // Copy array
    const shuffled = [...suggestedQuestions];


    // Shuffle questions
    shuffled.sort(() => Math.random() - 0.5);


    // Select 7 random questions
    const selectedQuestions = shuffled.slice(0, 7);


    // Clear old questions
    container.innerHTML = "";


    // Create buttons
    selectedQuestions.forEach(item => {

        const button = document.createElement("button");

        button.innerHTML = `
            ${item.icon} ${item.question}
        `;


        button.onclick = function() {

            askQuickQuestion(item.question);

        };


        container.appendChild(button);

    });

}
// =====================================================
// CONFIGURATION
// =====================================================

const API_URL = "http://127.0.0.1:8000/chat";


// =====================================================
// ELEMENTS
// =====================================================

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const typingIndicator = document.getElementById("typingIndicator");


// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage() {

    const question = userInput.value.trim();

    if (!question) {
        return;
    }


    // Remove welcome screen
    const welcome = document.querySelector(".welcome-message");

    if (welcome) {
        welcome.remove();
    }


    // Show user message
    addMessage(question, "user");


    // Clear input
    userInput.value = "";


    // Show typing indicator
    typingIndicator.classList.remove("hidden");


    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const data = await response.json();


        // Hide typing
        typingIndicator.classList.add("hidden");


        if (data.success) {

            addMessage(data.answer, "bot");

        } else {

            addMessage(
                data.answer || "Sorry, something went wrong.",
                "bot"
            );

        }

    } catch (error) {

        console.error(error);

        typingIndicator.classList.add("hidden");

        addMessage(
            "Unable to connect to the Home Assistant server. Please make sure the FastAPI backend is running.",
            "bot"
        );

    }

}


// =====================================================
// ADD MESSAGE
// =====================================================

function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;


    const content = document.createElement("div");

    content.className = "message-content";


    // Preserve line breaks
    content.style.whiteSpace = "pre-wrap";

    content.textContent = text;


    message.appendChild(content);

    chatMessages.appendChild(message);


    // Scroll to latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// =====================================================
// QUICK QUESTION
// =====================================================

function askQuickQuestion(question) {

    userInput.value = question;

    sendMessage();

}


// =====================================================
// NEW CHAT
// =====================================================

function newChat() {

    chatMessages.innerHTML = `

        <div class="welcome-message">

            <div class="welcome-icon">
                🏡
            </div>

            <h2>
                Welcome Home!
            </h2>

            <p>
                I can help you manage household
                expenses, bills, groceries and family tasks.
            </p>

            <div class="suggestions">

                <button onclick="askQuickQuestion(
                    'What are my pending family tasks?'
                )">
                    📋 Pending tasks
                </button>

                <button onclick="askQuickQuestion(
                    'How much was the electricity bill in June?'
                )">
                    ⚡ Electricity bill
                </button>

                <button onclick="askQuickQuestion(
                    'How much did we spend on groceries?'
                )">
                    🛒 Grocery expenses
                </button>

            </div>

        </div>

    `;

}


// =====================================================
// ENTER KEY
// =====================================================

userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});

showRandomQuestions();