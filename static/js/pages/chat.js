let eventSource;
const sseData = document.getElementById('id_sse_messsages');

function startSSE() {
    eventSource = new EventSource(`/stream-chat-messages/${window.location.pathname.split('/')[2]}`)
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageHTML  = `
        <div class="chat__message">
            <div class="chat__message-info">
                <p class="chat__message-sender">${data.author__user__username}</p>
                <p class="chat__message-date">${data.created}</p>
            </div>
            <p class="chat__message-content">${data.content}</p>
        </div>
        `
        sseData.innerHTML += messageHTML;
    }
}


$(document).ready(function () {
    startSSE();
});