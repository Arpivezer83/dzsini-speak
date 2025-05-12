const chatBox = document.getElementById('chat-box');
const startBtn = document.getElementById('start-btn');
const sendBtn = document.getElementById('send-btn');
const textInput = document.getElementById('text-input');

function appendMessage(role, text) {
  const div = document.createElement('div');
  div.className = role;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(message) {
  appendMessage('user', message);
  textInput.value = '';

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer my-secret-token'
      },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
   console.log('Szerver válasza:', data);

    appendMessage('ai', data.reply || data.response || '[no response]');
  } catch (err) {
    appendMessage('ai', '⚠️ Error talking to Dzsini.');
    console.error(err);
  }
}
sendBtn.addEventListener('click', () => {
  const message = textInput.value.trim();
  if (message) sendMessage(message);
});

textInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendBtn.click();
});

startBtn.addEventListener('click', () => {
  alert('🎤 Microphone input coming soon!');
});
