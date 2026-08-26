const form = document.querySelector("#resume-form");
const resumeInput = document.querySelector("#resume");
const fileName = document.querySelector("#file-name");

resumeInput.addEventListener("change", () => {
    if (resumeInput.files.length > 0) {
        fileName.textContent = resumeInput.files[0].name;
    }
});

function showSkills(elementId, skills, isMissing = false) {
    const element = document.querySelector(elementId);

    if (skills.length === 0) {
        element.innerHTML = "<p>No skills detected.</p>";
        return;
    }

    element.innerHTML = skills.map(skill => {
        const className = isMissing
            ? "skill missing-skill"
            : "skill";

        return `<span class="${className}">${skill}</span>`;
    }).join("");
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    const loading = document.querySelector("#loading");
    const results = document.querySelector("#results");

    loading.classList.remove("hidden");
    results.classList.add("hidden");

    const formData = new FormData();

    formData.append("resume", resumeInput.files[0]);
    formData.append(
        "job_description",
        document.querySelector("#job-description").value
    );

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not analyze resume.");
        }

        document.querySelector("#score").textContent = data.score;

        document.querySelector("#score-text").textContent =
            `Semantic similarity: ${data.semantic_similarity}%. ` +
            `Matched ${data.matched_skills.length} skill(s).`;

        showSkills("#matched-skills", data.matched_skills);
        showSkills(
            "#missing-skills",
            data.missing_skills,
            true
        );

        document.querySelector("#suggestions").innerHTML =
            data.suggestions
                .map(item => `<li>${item}</li>`)
                .join("");

        document.querySelector("#experience").innerHTML =
            data.relevant_experience.length
                ? data.relevant_experience
                    .map(item => `<li>${item}</li>`)
                    .join("")
                : "<li>No relevant experience line found.</li>";

        results.classList.remove("hidden");
    } catch (error) {
        alert(error.message);
    } finally {
        loading.classList.add("hidden");
    }
});