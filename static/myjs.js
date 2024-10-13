let topic_changed = false;

async function regenerateQuestion() {
    const topicButton = document.getElementById('topic-submit');
    const container = document.getElementById('topic-suggestions');
    const question = document.getElementById('question');
    const prev_question = question.innerText; 
    question.setAttribute('aria-busy', 'true');
    // Empty old data

    question.innerText = '';
    if (topic_changed) {
        container.innerHTML = '';
    }

    topicButton.disabled = true;  // Disable the button

    // Prepare the request data
    const topic = document.getElementById('topic');
    const attributes = document.getElementById('attributes');
    const style = document.getElementById('style')
    const fileInput = document.getElementById('file-input')
    const is_file = fileInput.files.length > 0
    const data = { topic: topic.value , attributes: attributes.value, is_file: is_file, style: style.value, is_new_topic: topic_changed};
    // Create the requests
    const questionRequest = fetch('/generatequestion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    let suggestionRequest = null;
    if (topic_changed) {
        suggestionRequest = fetch('/topicsuggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
    }

    // Wait for both requests simultaneously
    const [questionResponse, suggestionResponse] = await Promise.all([
        questionRequest,
        suggestionRequest
    ]);

    // Handle the question response
    const questionData = await questionResponse.json();
    question.innerText = questionData.question;

    // Handle the suggestions response (if topic has changed)
    if (topic_changed && suggestionResponse) {
        const suggestionData = await suggestionResponse.json();
        suggestionData.topic_suggestions.forEach(topic_suggestion => {
            const button = document.createElement('button');
            button.innerText = topic_suggestion;
            button.setAttribute('onclick', 'selectNewTopicButton(this)');
            container.appendChild(button);
        });
        topic_changed = false;
    }

    // Re-enable the button after all requests are done
    topicButton.disabled = false;
    question.setAttribute('aria-busy', 'false');
}


function selectNewTopicButton(button) {
    const buttonText = button.innerText;
    const input = document.getElementById('topic');
    input.value = buttonText;
    topic_changed = true;
    regenerateQuestion();
}

function updateChanged() {
    topic_changed = true;
}

async function uploadFile(fileElement){
    topic_changed = true;
    fileElement.disabled = true
    const removeFileButton = document.getElementById('remove-file');
    removeFileButton.style = 'display:block'
    removeFileButton.innerText = ''
    removeFileButton.setAttribute('aria-busy','true')
    const formData = new FormData();
    formData.append("file", fileElement.files[0]);
    const result = await fetch('/uploadfile', {
        method: 'POST',
        body: formData
    });
    fileElement.disabled = false
    removeFileButton.innerHTML = '&#x2715;'
    removeFileButton.setAttribute('aria-busy','false')
}

async function removeFile(removeFileButton){
    topic_changed = true;
    const fileElement = document.getElementById('file-input');
    fileElement.disabled = true
    removeFileButton.style = 'display:none'
    removeFileButton.innerText = ''
    removeFileButton.setAttribute('aria-busy','true')
    // Send detele request for file 
    const fileName = fileElement.files[0].name;
    await fetch(`/deletefile/${fileName}`, {
        method: 'DELETE',
    });
    // Re-enable input
    fileElement.value = "";
    fileElement.disabled = false
    removeFileButton.setAttribute('aria-busy','false')
}