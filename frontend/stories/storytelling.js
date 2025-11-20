// API Endpoint
const API_URL = "/api/stories";

let stories = [];   // global array
let currentChart;   // for Chart.js cleanup

// Load stories from backend
async function loadStories() {
    try {
        const res = await fetch(API_URL);
        stories = await res.json();
        renderTags();
        renderCards(stories);
    } catch (err) {
        console.error("Failed to load stories:", err);
    }
}

// Render tags dynamically
function renderTags() {
    const allTags = [...new Set(stories.flatMap(s => s.tags))];
    const tagDiv = document.getElementById("tagsContainer");

    tagDiv.innerHTML = allTags
        .map(tag => `<button class="tag-btn" data-tag="${tag}">#${tag}</button>`)
        .join("");

    // Tag click filter
    tagDiv.addEventListener("click", (e) => {
        if (e.target.classList.contains("tag-btn")) {
            const tag = e.target.dataset.tag;
            const filtered = stories.filter(s => s.tags.includes(tag));
            renderCards(filtered);
        }
    });
}

// Render story cards
function renderCards(list) {
    const grid = document.getElementById("storiesGrid");

    if (list.length === 0) {
        grid.innerHTML = "<p>No stories found.</p>";
        return;
    }

    grid.innerHTML = list.map(cardHTML).join("");

    // Add click event to each read-more button
    document.querySelectorAll(".read-more").forEach(btn => {
        btn.addEventListener("click", () => {
            openStory(btn.dataset.id);
        });
    });
}

// Card template
function cardHTML(s) {
    return `
        <div class="card">
            <img src="${s.image}" alt="${s.title}" />
            <h3>${s.title}</h3>
            <p>${s.points.slice(0, 2).join(" • ")}</p>

            <div class="tags">
                ${s.tags.map(t => `<span>#${t}</span>`).join("")}
            </div>

            <button class="read-more" data-id="${s.id}">Read More</button>
        </div>
    `;
}

// Open modal with full story
async function openStory(id) {
    const res = await fetch(`${API_URL}/${id}`);
    const story = await res.json();

    const modal = document.getElementById("storyModal");
    const modalBody = document.getElementById("modalBody");

    modalBody.innerHTML = `
        <h2>${story.title}</h2>
        <p>${story.summary}</p>

        <ul>
            ${story.points.map(p => `<li>${p}</li>`).join("")}
        </ul>
    `;

    modal.classList.remove("hidden");

    loadChart(story.chart);
}

// Load Chart.js
function loadChart(chartData) {
    const ctx = document.getElementById("storyChart").getContext("2d");

    // Destroy old chart if open
    if (currentChart) {
        currentChart.destroy();
    }

    currentChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: "Travel Insights",
                    data: chartData.data,
                    backgroundColor: "rgba(0, 123, 255, 0.6)",
                    borderColor: "#003366",
                    borderWidth: 1
                }
            ]
        }
    });
}

// Close modal
document.getElementById("closeModal").addEventListener("click", () => {
    document.getElementById("storyModal").classList.add("hidden");
});

// Search feature
document.getElementById("search").addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase();
    const result = stories.filter(
        s =>
            s.title.toLowerCase().includes(q) ||
            s.country.toLowerCase().includes(q) ||
            s.tags.some(t => t.toLowerCase().includes(q))
    );
    renderCards(result);
});

// Load stories when page opens
loadStories();
