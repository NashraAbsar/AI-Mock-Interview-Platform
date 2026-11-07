
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

let performanceChart = null;
let topicChart = null;

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


// Load and display interview history with analytics
historyButton.addEventListener("click", async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        message.textContent = "Please log in to view your interview history.";
        return;
    }

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

        // Collect only evaluated answers with valid numeric scores
        const scoredAnswers = interviews.flatMap(interview =>
            (interview.answers || [])
                .filter(answer =>
                    answer.score !== null &&
                    answer.score !== undefined &&
                    Number.isFinite(Number(answer.score))
                )
                .map(answer => ({
                    ...answer,
                    topic: interview.topic || "Other"
                }))
        );

        const scores = scoredAnswers.map(answer => Number(answer.score));

        const averageScore = scores.length
            ? scores.reduce((sum, score) => sum + score, 0) / scores.length
            : 0;

        const highestScore = scores.length
            ? Math.max(...scores)
            : 0;

        // Calculate average score for each interview
        const interviewAverages = interviews.map(interview => {
            const interviewScores = (interview.answers || [])
                .filter(answer =>
                    answer.score !== null &&
                    answer.score !== undefined &&
                    Number.isFinite(Number(answer.score))
                )
                .map(answer => Number(answer.score));

            const average = interviewScores.length
                ? interviewScores.reduce((sum, score) => sum + score, 0)
                    / interviewScores.length
                : null;

            return {
                label: `${interview.role} (${new Date(interview.created_at).toLocaleDateString()})`,
                average
            };
        }).filter(item => item.average !== null).reverse();

        // Calculate average score topic-wise
        const topicScores = {};

        scoredAnswers.forEach(answer => {
            if (!topicScores[answer.topic]) {
                topicScores[answer.topic] = [];
            }

            topicScores[answer.topic].push(Number(answer.score));
        });

        const topicLabels = Object.keys(topicScores);

        const topicAverages = topicLabels.map(topic => {
            const values = topicScores[topic];

            return values.reduce((sum, score) => sum + score, 0)
                / values.length;
        });

        // Display analytics and interview history
        historyContainer.innerHTML = `
            <div class="analytics-heading">
                <p class="eyebrow">YOUR PERFORMANCE</p>
                <h2>Interview Analytics</h2>
                <p>Track your practice activity and monitor your progress.</p>
            </div>

            <div class="analytics-summary">
                <div class="analytics-card">
                    <p>Total Interviews</p>
                    <h3>${interviews.length}</h3>
                </div>

                <div class="analytics-card">
                    <p>Average Score</p>
                    <h3>${scores.length ? averageScore.toFixed(1) : "—"}</h3>
                </div>

                <div class="analytics-card">
                    <p>Highest Score</p>
                    <h3>${scores.length ? highestScore : "—"}</h3>
                </div>
            </div>

            <div class="analytics-charts">
                <div class="chart-card">
                    <h3>Interview Performance</h3>
                    <div class="chart-container">
                        <canvas id="performanceChart"></canvas>
                    </div>
                    ${interviewAverages.length === 0
                        ? "<p>No evaluated interviews available for the chart yet.</p>"
                        : ""}
                </div>

                <div class="chart-card">
                    <h3>Topic-wise Score Analysis</h3>
                    <div class="chart-container">
                        <canvas id="topicChart"></canvas>
                    </div>
                    ${topicLabels.length === 0
                        ? "<p>No topic scores available yet.</p>"
                        : ""}
                </div>
            </div>

            <h2>Interview History</h2>
            ${interviews.length === 0
    ? "<p>No previous interviews found. Start your first interview!</p>"
    : interviews.map((interview, index) => `
        <div class="history-card">
            <h3>${interview.role} — ${interview.topic}</h3>

            <p><strong>Experience:</strong>
                ${interview.experience_level}
            </p>

            <p><strong>Date:</strong>
                ${new Date(interview.created_at).toLocaleString()}
            </p>

            <p><strong>Answers Submitted:</strong>
                ${(interview.answers || []).length}
            </p>

            ${(interview.answers || []).length > 0
                ? `
                    <button
                        type="button"
                        class="view-answers-button"
                        data-interview-index="${index}"
                        aria-expanded="false"
                    >
                        View Interview Answers
                    </button>

                    <div
                        class="interview-answers"
                        id="interview-answers-${index}"
                        hidden
                    >
                        ${interview.answers.map((answer, answerIndex) => `
                            <div class="history-answer">
                                <h4>Question ${answerIndex + 1}</h4>

                                <p><strong>Question:</strong>
                                    ${answer.question}
                                </p>

                                <p><strong>Your answer:</strong>
                                    ${answer.answer}
                                </p>

                                <p><strong>Score:</strong>
                                    ${answer.score ?? "Not evaluated"}
                                </p>

                                <p><strong>Feedback:</strong>
                                    ${answer.feedback ?? "Not available"}
                                </p>
                            </div>
                        `).join("")}
                    </div>
                `
                : "<p>No answers submitted for this interview.</p>"
            }
        </div>
    `).join("")
}
        `;

        // Show or hide answers for individual interviews
document.querySelectorAll(".view-answers-button").forEach(button => {
    button.addEventListener("click", () => {
        const index = button.dataset.interviewIndex;
        const answersContainer = document.getElementById(
            `interview-answers-${index}`
        );

        const isHidden = answersContainer.hidden;

        answersContainer.hidden = !isHidden;
        button.setAttribute("aria-expanded", String(isHidden));

        button.textContent = isHidden
            ? "Hide Interview Answers"
            : "View Interview Answers";
    });
});

        // Remove old charts before creating new ones
        if (performanceChart) {
            performanceChart.destroy();
            performanceChart = null;
        }

        if (topicChart) {
            topicChart.destroy();
            topicChart = null;
        }

        // Create interview performance line chart
        if (typeof Chart !== "undefined" && interviewAverages.length > 0) {
            performanceChart = new Chart(
                document.getElementById("performanceChart"),
                {
                    type: "line",
                    data: {
                        labels: interviewAverages.map(item => item.label),
                        datasets: [{
                            label: "Average Score",
                            data: interviewAverages.map(item => item.average),
                            borderColor: "#6d4aff",
                            backgroundColor: "rgba(109, 74, 255, 0.12)",
                            fill: true,
                            tension: 0.35,
                            pointRadius: 5
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                }
            );
        }

        // Create topic-wise bar chart
        if (typeof Chart !== "undefined" && topicLabels.length > 0) {
            topicChart = new Chart(
                document.getElementById("topicChart"),
                {
                    type: "bar",
                    data: {
                        labels: topicLabels,
                        datasets: [{
                            label: "Average Score",
                            data: topicAverages,
                            backgroundColor: "#8a70f5",
                            borderRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                }
            );
        }

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
