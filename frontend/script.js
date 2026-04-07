async function loadSummaries() {
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = 'Loading...';
    try {
        // Use the FastAPI service name inside Docker network
        const response = await fetch('/api/summaries');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (data.length === 0) {
            contentDiv.innerHTML = '<p>No summaries found. Run the Airflow DAG first.</p>';
            return;
        }
        let html = '';
        data.forEach(article => {
            html += `
                <div class="article">
                    <div class="title">${escapeHtml(article.title)}</div>
                    <div class="summary">${escapeHtml(article.summary)}</div>
                    <div class="meta">Published: ${article.published_at} | <a href="${article.url}" target="_blank">Source</a></div>
                </div>
            `;
        });
        contentDiv.innerHTML = html;
    } catch (err) {
        contentDiv.innerHTML = `<p class="error">Error: ${err.message}</p>`;
    }
}

function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

document.getElementById('refreshBtn').addEventListener('click', loadSummaries);