// const API_BASE_URL = 'http://localhost:8000';
// let currentConversation = null;

// document.addEventListener('DOMContentLoaded', () => {
//   const token = localStorage.getItem('token');
//   if (!token) {
//     window.location.href = 'auth.html';
//   } else {
//     initChatPage();
//   }
// });

// async function initChatPage() {
//   const email = localStorage.getItem('user_email');
//   document.getElementById('user-email').textContent = email;

//   await loadConversations();
//   if (!currentConversation) {
//     await createNewConversation();
//   }

//   document.getElementById('logout-btn').addEventListener('click', () => {
//     localStorage.removeItem('token');
//     localStorage.removeItem('user_email');
//     window.location.href = 'auth.html';
//   });

//   document.getElementById('new-chat-btn').addEventListener('click', createNewConversation);

//   document.getElementById('chat-form').addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const input = document.getElementById('chat-input');
//     const query = input.value.trim();
//     if (!query) return;

//     addMessage('user', query);
//     currentConversation.messages.push({ role: 'user', content: query });
//     if (currentConversation.title === 'New Chat') {
//       currentConversation.title = `Chat ${new Date().toISOString().slice(0, 10)} - ${query.slice(0, 20)}`;
//       console.log('New title set:', currentConversation.title);
//     }
//     await saveConversation();
//     input.value = '';
//     document.getElementById('chat-form').querySelector('button').disabled = true;

//     try {
//       const token = localStorage.getItem('token');
//       if (!token) throw new Error('No authentication token found');

//       const response = await fetch(`${API_BASE_URL}/research/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${token}`,
//         },
//         body: JSON.stringify({ topic: query, max_results: 5 }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to fetch research');
//       }

//       const data = await response.json();
//       const content = {
//         summary: linkCitations(data.summary, data.sources),
//         sources: data.sources,
//       };
//       addMessage('assistant', content);
//       currentConversation.messages.push({ role: 'assistant', content });
//       await saveConversation();
//     } catch (error) {
//       addMessage('assistant', { summary: `<p>${error.message}</p>` });
//       currentConversation.messages.push({ role: 'assistant', content: error.message });
//       await saveConversation();
//     } finally {
//       document.getElementById('chat-form').querySelector('button').disabled = false;
//     }
//   });
// }

// function linkCitations(summary, sources) {
//   let linkedSummary = marked.parse(summary);
//   sources.forEach((source, index) => {
//     const citation = `[${index + 1}]`;
//     const link = `<a href="${source.link}" target="_blank" class="citation">${index + 1}</a>`;
//     linkedSummary = linkedSummary.replace(citation, link);
//   });
//   return linkedSummary;
// }

// async function getConversations() {
//   const token = localStorage.getItem('token');
//   try {
//     const response = await fetch(`${API_BASE_URL}/chats/conversations`, {
//       headers: {
//         'Authorization': `Bearer ${token}`,
//       },
//     });
//     if (!response.ok) throw new Error('Failed to fetch conversations');
//     const data = await response.json();
//     console.log('API response for conversations:', data);
//     return data;
//   } catch (error) {
//     console.error('Error fetching conversations:', error);
//     return [];
//   }
// }

// async function saveConversation() {
//   const token = localStorage.getItem('token');
//   try {
//     const response = await fetch(`${API_BASE_URL}/chats/store_conversations`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'Authorization': `Bearer ${token}`,
//       },
//       body: JSON.stringify({
//         title: currentConversation.title,
//         messages: currentConversation.messages,
//       }),
//     });
//     if (!response.ok) throw new Error('Failed to save conversation');
//     const data = await response.json();
//     console.log('Saved conversation response:', data);
//     currentConversation.id = data.id;
//   } catch (error) {
//     console.error('Error saving conversation:', error);
//   }
// }

// async function createNewConversation() {
//   currentConversation = {
//     id: null,
//     title: 'New Chat',
//     messages: [],
//   };
//   await saveConversation();
//   await updateConversationList();
//   renderMessages();
// }

// async function loadConversations() {
//   const conversations = await getConversations();
//   console.log('Loaded conversations:', conversations);
//   if (conversations.length > 0) {
//     currentConversation = conversations[0];
//   }
//   await updateConversationList();
//   renderMessages();
// }

// async function updateConversationList() {
//   const list = document.getElementById('conversation-list');
//   list.innerHTML = '';
//   const conversations = await getConversations();
//   console.log('Conversations to render:', conversations);
//   if (conversations.length === 0) {
//     const div = document.createElement('div');
//     div.className = 'conversation-item';
//     div.textContent = 'No conversations yet';
//     div.style.color = '#9ca3af';
//     list.appendChild(div);
//   } else {
//     conversations.forEach((conv) => {
//       const div = document.createElement('div');
//       div.className = 'conversation-item';
//       div.innerHTML = `
//         <span title="${conv.title}" class="conversation-title">${conv.title}</span>
//         <button class="delete-btn" title="Delete conversation">🗑️</button>
//       `;
//       div.querySelector('.conversation-title').addEventListener('click', () => {
//         currentConversation = conv;
//         renderMessages();
//       });
//       div.querySelector('.delete-btn').addEventListener('click', async (e) => {
//         e.stopPropagation();
//         await deleteConversation(conv.id);
//       });
//       list.appendChild(div);
//     });
//   }
// }

// async function deleteConversation(id) {
//   const token = localStorage.getItem('token');
//   try {
//     const response = await fetch(`${API_BASE_URL}/chats/delete_conversations/${id}`, {
//       method: 'DELETE',
//       headers: {
//         'Authorization': `Bearer ${token}`,
//       },
//     });
//     if (!response.ok) {
//       const errorData = await response.json();
//       throw new Error(errorData.detail || 'Failed to delete conversation');
//     }
//     if (currentConversation && currentConversation.id === id) {
//       const conversations = await getConversations();
//       currentConversation = conversations.length > 0 ? conversations[0] : null;
//       if (!currentConversation) {
//         await createNewConversation();
//       }
//     }
//     await updateConversationList();
//     renderMessages();
//   } catch (error) {
//     console.error('Error deleting conversation:', error);
//     alert(`Error: ${error.message}`);
//   }
// }

// function addMessage(role, content) {
//   const messages = document.getElementById('chat-messages');
//   const div = document.createElement('div');
//   div.className = `message ${role}`;
//   if (typeof content === 'string') {
//     div.innerHTML = `<p>${content}</p>`;
//   } else {
//     div.innerHTML = content.summary;
//   }
//   messages.appendChild(div);
//   messages.scrollTop = messages.scrollHeight;
// }

// function renderMessages() {
//   const messages = document.getElementById('chat-messages');
//   messages.innerHTML = '';
//   if (currentConversation) {
//     currentConversation.messages.forEach((msg) => addMessage(msg.role, msg.content));
//   }
// }




const API_BASE_URL = 'http://localhost:8000';
let currentConversation = {
  id: null,
  title: 'Current Chat',
  messages: []
};

document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = 'auth.html';
  } else {
    initChatPage();
  }
});

async function initChatPage() {
  const email = localStorage.getItem('user_email');
  document.getElementById('user-email').textContent = email;

  document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_email');
    window.location.href = 'auth.html';
  });

  document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = document.getElementById('chat-input');
    const query = input.value.trim();
    if (!query) return;

    addMessage('user', query);
    currentConversation.messages.push({ role: 'user', content: query });
    await saveConversation();
    input.value = '';
    document.getElementById('chat-form').querySelector('button').disabled = true;

    try {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('No authentication token found');

      const response = await fetch(`${API_BASE_URL}/research/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ topic: query, max_results: 5 }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch research');
      }

      const data = await response.json();
      const content = {
        summary: linkCitations(data.summary, data.sources),
        sources: data.sources,
      };
      addMessage('assistant', content);
      currentConversation.messages.push({ role: 'assistant', content });
      await saveConversation();
    } catch (error) {
      addMessage('assistant', { summary: `<p>${error.message}</p>` });
      currentConversation.messages.push({ role: 'assistant', content: error.message });
      await saveConversation();
    } finally {
      document.getElementById('chat-form').querySelector('button').disabled = false;
    }
  });
}

function linkCitations(summary, sources) {
  let linkedSummary = marked.parse(summary);
  sources.forEach((source, index) => {
    const citation = `[${index + 1}]`;
    const link = `<a href="${source.link}" target="_blank" class="citation">[${index + 1}]</a>`;
    linkedSummary = linkedSummary.replace(new RegExp(`\\${citation}`, 'g'), link);
  });
  return linkedSummary;
}

async function saveConversation() {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_BASE_URL}/chats/store_conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: currentConversation.title,
        messages: currentConversation.messages,
      }),
    });
    if (!response.ok) throw new Error('Failed to save conversation');
    const data = await response.json();
    console.log('Saved conversation:', data);
    currentConversation.id = data.id;
  } catch (error) {
    console.error('Error saving conversation:', error);
  }
}

function addMessage(role, content) {
  const messages = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = `message ${role}`;
  if (typeof content === 'string') {
    div.innerHTML = `<p>${content}</p>`;
  } else {
    div.innerHTML = content.summary;
  }
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function renderMessages() {
  const messages = document.getElementById('chat-messages');
  messages.innerHTML = '';
  currentConversation.messages.forEach((msg) => addMessage(msg.role, msg.content));
}