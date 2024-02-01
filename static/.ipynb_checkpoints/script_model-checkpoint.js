const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input #send-btn");


// Create the Generate Codes button outside of the chat messages
const genCodesBtn = document.createElement("button");
genCodesBtn.textContent = "Create the jobs & continue";
genCodesBtn.classList.add("sui-a-button", "as--primary"); // Add the CSS class
chatbox.appendChild(genCodesBtn);

// Create the Create in Saagie button outside of the chat messages
const createInSaagieBtn = document.createElement("button");
createInSaagieBtn.textContent = "Create the Pipeline & the Jobs in Saagie";
createInSaagieBtn.classList.add("sui-a-button", "as--primary"); // Add the CSS class
chatbox.appendChild(createInSaagieBtn);

// Select all buttons within the chatbox
const buttonsInChatbox = chatbox.querySelectorAll("button.sui-a-button");
// Hide all buttons
buttonsInChatbox.forEach(button => {
    button.style.display = "none";
});

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = '';
    if (className === "outgoing") {
        //chatContent = `<p></p></div><span>\n<img class="avatar" src="static/me_avatar.svg">\n</span>`;
        //chatContent = `<p></p></div><span>\n<img class="avatar" src="static/me_avatar.svg">\n</span>`;
        chatContent = `<p></p></div><div class="sui-a-avatar as--you">\n<Icon name="user" />\n</div>`;
    } else {
        chatContent = `<span>\n<img class="avatar" src="static/saagie_avatar.svg">\n</span><p></p>`;
    }
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}

const generatePipelineDecomposition = async (chatElement, userMessage) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('/generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "pipeline_decomposition", "user_message": userMessage }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch response");
        }

        const data = await response.json();

        // Extract the desired fields from each dictionary
        const extractedFields = data.map(item => {
            
            //return `<strong>Job ${item.id} : ${item.name}</strong>\nDescription: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n`;
            return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n</div>`;
        });

        // Join the extracted fields into a single message
        const messageText = extractedFields.join('\n');

        // Set the response message from the server
        messageElement.innerHTML = messageText;
        
        // Show the button after the response is generated
        genCodesBtn.style.display = "block";
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    } finally {
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
}

const generateCodeGeneration = async (chatElement) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('/generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "code_generation", "user_message": "" }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch response");
        }

        
        const data = await response.json();

        // Extract the desired fields from each dictionary
        const extractedFields = data.map(item => {
            return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n<pre><code class="python hljs">${item.code}</code></pre>`;
        });

        // Join the extracted fields into a single message
        const messageText = extractedFields.join('\n');

        // Set the response message from the server
        messageElement.innerHTML = messageText;
        
        // Show the button for the API
        createInSaagieBtn.style.display = "block";
        
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
        // Display the genCodesBtn if the creation in Saagie failed
        genCodesBtn.style.display = "block";
    } finally {
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
}

const generateCreationInSaagie = async (chatElement) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('/generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "creation_in_saagie", "user_message": "" }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch response");
        }
        
        const reader = response.body.getReader();

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            const job = value.response;

            // Extract the desired fields from each job
            const extractedFields = `<div class="sui-a-text as--ml">Job ${job.id} : ${job.name}</div>\n<div class="sui-a-text">Description: ${job.description}\nInput Resources: ${JSON.stringify(job.input_resources)}\nOutput Resources: ${JSON.stringify(job.output_resources)}\n\n<pre><code class="python hljs">${job.code}</code></pre>`;

            // Append the extracted fields to the chatbox
            const messageElement = document.createElement("div");
            messageElement.innerHTML = extractedFields;
            messageElement.classList.add("incoming");

            // Set the response message from the server
            chatElement.appendChild(messageElement);

            // Show the button for the API
            createInSaagieBtn.style.display = "block";

            // Scroll to the latest message
            chatbox.scrollTo(0, chatbox.scrollHeight);
        }
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
        // Display the createInSaagieBtn if the creation in Saagie failed
        createInSaagieBtn.style.display = "block";
    }
}
/*
        const data = await response.json();

        // Extract the result content from data
        const messageText = `<div class="sui-a-text">${data.result}</div>`;

        // Set the response message from the server
        messageElement.innerHTML = messageText;
        
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
        // Display the createInSaagieBtn if the creation in Saagie failed
        createInSaagieBtn.style.display = "block";
    } finally {
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
}
*/


const handleChat = async () => {
    // Hide all buttons
    buttonsInChatbox.forEach(button => {
        button.style.display = "none";
    });
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    const outgoingChatLi = createChatLi(userMessage, "outgoing");
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);


    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    // Generate the response
    await generatePipelineDecomposition(incomingChatLi, userMessage);

}

const handleCodeGeneration = async () => {
    // Hide all buttons
    buttonsInChatbox.forEach(button => {
        button.style.display = "none";
    });
    userMessage = "Generate the codes please";

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    const outgoingChatLi = createChatLi(userMessage, "outgoing");
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);


    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    // Generate the response
    await generateCodeGeneration(incomingChatLi);
}

const handleCreationInSaagie = async () => {
    // Hide all buttons
    buttonsInChatbox.forEach(button => {
        button.style.display = "none";
    });

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Creating the Pipeline & Jobs in Saagie...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    // Generate the response
    await generateCreationInSaagie(incomingChatLi);
}


chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", () => {
        handleChat();
});

genCodesBtn.addEventListener("click", () => {
    handleCodeGeneration();
});

createInSaagieBtn.addEventListener("click", () => {
    handleCreationInSaagie();
});