
const loginSection = document.getElementById("loginSection");
const registerSection = document.getElementById("registerSection");
const setupSection = document.getElementById("setupSection");
const questionsSection = document.getElementById("questionsSection");
const questionsContainer = document.getElementById("questionsContainer");
const historySection = document.getElementById("historySection");
const historyContainer = document.getElementById("historyContainer");
const message = document.getElementById("message");

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const interviewForm = document.getElementById("interviewForm");

const historyButton = document.getElementById("historyButton");
const logoutButton = document.getElementById("logoutButton");
const newInterviewButton = document.getElementById("newInterviewButton");

// Switch to Registration
document.getElementById("showRegisterButton").addEventListener("click", () => {
    loginSection.hidden = true;
    registerSection.hidden = false;
    message.textContent = "";
});

// Switch to Login
document.getElementById("showLoginButton").addEventListener("click", () => {
    registerSection.hidden = true;
    loginSection.hidden = false;
    message.textContent = "";
});

// Register a new user
registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;

    message.textContent = "Creating your account...";

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail)
            );
        }

        registerForm.reset();
        registerSection.hidden = true;
        loginSection.hidden = false;
        document.getElementById("email").value = email;

        message.textContent = "Account created! Please log in.";
    } catch (error) {
        message.textContent = error.message;
    }
});

// Login existing user
loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    message.textContent = "Logging in...";

    try {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Login failed.");
        }

        localStorage.setItem("access_token", data.access_token);

        loginSection.hidden = true;
        registerSection.hidden = true;
        setupSection.hidden = false;
        questionsSection.hidden = true;
        historySection.hidden = true;
        logoutButton.hidden = false;

        historyContainer.innerHTML = "";
        message.textContent = "Login successful! Set up your interview.";
    } catch (error) {
        message.textContent = error.message;
    }
});

// Create interview and load questions
interviewForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const role = document.getElementById("role").value.trim();
    const experienceLevel = document.getElementById("experienceLevel").value;
    const topic = document.getElementById("topic").value;
    const startButton = document.getElementById("startButton");
    const token = localStorage.getItem("access_token");

    if (!token) {
        message.textContent = "Please log in before starting an interview.";
        return;
    }

    message.textContent = "Creating your interview...";
    startButton.disabled = true;

    try {
        const response = await fetch("/interviews", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                role,
                experience_level: experienceLevel,
                topic
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not create interview.");
        }

        const questionsResponse = await fetch(
            `/interviews/${data.id}/questions`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const questionsData = await questionsResponse.json();

        if (!questionsResponse.ok) {
            throw new Error(
                questionsData.detail || "Could not load interview questions."
            );
        }

        questionsContainer.innerHTML = `
            <h2>Your Interview Questions</h2>
            <p><strong>Role:</strong> ${data.role}</p>
            <p><strong>Topic:</strong> ${data.topic}</p>

            ${questionsData.questions.map((question, index) => `
                <div class="question-card">
                    <h3>Question ${index + 1}</h3>
                    <p>${question}</p>

                    <textarea
                        id="answer-${index}"
                        placeholder="Type your answer here..."
                        rows="5"
                        required
                    ></textarea>

                    <button
                        type="button"
                        class="submit-answer-button"
                        data-index="${index}"
                    >
                        Submit Answer
                    </button>

                    <div id="feedback-${index}"></div>
                </div>
            `).join("")}
        `;

        setupSection.hidden = true;
        historySection.hidden = true;
        questionsSection.hidden = false;

        // Attach answer submission handlers
        document.querySelectorAll(".submit-answer-button").forEach(button => {
            button.addEventListener("click", async () => {
                const index = Number(button.dataset.index);
                const question = questionsData.questions[index];
                const answer = document.getElementById(`answer-${index}`).value.trim();
                const feedback = document.getElementById(`feedback-${index}`);

                if (!answer) {
                    feedback.textContent = "Please write your answer first.";
                    return;
                }

                button.disabled = true;
                feedback.textContent = "Submitting and evaluating your answer...";

                try {
                    const answerResponse = await fetch("/answers", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            session_id: data.id,
                            question,
                            answer
                        })
                    });

                    const answerData = await answerResponse.json();

                    if (!answerResponse.ok) {
                        throw new Error(
                            typeof answerData.detail === "string"
                                ? answerData.detail
                                : JSON.stringify(answerData.detail)
                        );
                    }

                    const evaluationResponse = await fetch(
                        `/answers/${answerData.id}/evaluate`,
                        {
                            method: "POST",
                            headers: {
                                "Authorization": `Bearer ${token}`
                            }
                        }
                    );

                    const evaluationData = await evaluationResponse.json();

                    if (!evaluationResponse.ok) {
                        throw new Error(
                            typeof evaluationData.detail === "string"
                                ? evaluationData.detail
                                : JSON.stringify(evaluationData.detail)
                        );
                    }

                    feedback.innerHTML = `
                        <p><strong>Score:</strong> ${evaluationData.score}</p>
                        <p><strong>Feedback:</strong> ${evaluationData.feedback}</p>
                    `;

                    button.textContent = "Answer Submitted";
                } catch (error) {
                    feedback.textContent = error.message;
                    button.disabled = false;
                }
            });
        });

        message.textContent = "Interview started successfully!";
    } catch (error) {
        message.textContent = error.message;
    } finally {
        startButton.disabled = false;
    }
});

// Load and display interview history
historyButton.addEventListener("click", async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        message.textContent = "Please log in to view your interview history.";
        return;
    }

    // Show history only after the user clicks the history button
    loginSection.hidden = true;
    registerSection.hidden = true;
    setupSection.hidden = true;
    questionsSection.hidden = true;
    historySection.hidden = false;
    logoutButton.hidden = false;

    historyContainer.innerHTML = "<p>Loading interview history...</p>";

    try {
        const response = await fetch("/interviews", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const interviews = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof interviews.detail === "string"
                    ? interviews.detail
                    : JSON.stringify(interviews.detail)
            );
        }

        if (interviews.length === 0) {
            historyContainer.innerHTML = "<p>No previous interviews found.</p>";
            return;
        }

        historyContainer.innerHTML = `
            <h2>Interview History</h2>
            ${interviews.map(interview => `
                <div class="history-card">
                    <h3>${interview.role} — ${interview.topic}</h3>
                    <p><strong>Experience:</strong> ${interview.experience_level}</p>
                    <p><strong>Date:</strong> ${new Date(interview.created_at).toLocaleString()}</p>

                    ${interview.answers.length > 0
                        ? interview.answers.map(answer => `
                            <div class="history-answer">
                                <p><strong>Question:</strong> ${answer.question}</p>
                                <p><strong>Your answer:</strong> ${answer.answer}</p>
                                <p><strong>Score:</strong> ${answer.score ?? "Not evaluated"}</p>
                                <p><strong>Feedback:</strong> ${answer.feedback ?? "Not available"}</p>
                            </div>
                        `).join("")
                        : "<p>No answers submitted for this interview.</p>"
                    }
                </div>
            `).join("")}
        `;
    } catch (error) {
        historyContainer.textContent = error.message;
    }
});

// Logout user
logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");

    loginSection.hidden = false;
    registerSection.hidden = true;
    setupSection.hidden = true;
    questionsSection.hidden = true;
    historySection.hidden = true;

    questionsContainer.innerHTML = "";
    historyContainer.innerHTML = "";
    logoutButton.hidden = true;

    loginForm.reset();
    interviewForm.reset();
    message.textContent = "";
});

// Start a new interview without logging out
newInterviewButton.addEventListener("click", () => {
    questionsContainer.innerHTML = "";
    questionsSection.hidden = true;
    historySection.hidden = true;
    setupSection.hidden = false;

    interviewForm.reset();
    message.textContent = "Set up your next interview.";
});
