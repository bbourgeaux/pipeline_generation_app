const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input #send-btn");
const restartBtn = document.querySelector(".restart-btn");

document.addEventListener("DOMContentLoaded", function() {
    const uploadImgBtn = document.getElementById("upload-img-btn");
    const fileUpload = document.getElementById("file-upload");

    // Trigger file input click when upload button is clicked
    uploadImgBtn.addEventListener("click", function() {
        fileUpload.click();
    });

    // Handle file selection
    fileUpload.addEventListener("change", function() {
        // Handle the file upload here
        const uploadedFile = fileUpload.files[0];
        console.log("Uploaded file:", uploadedFile);
        // You can perform further actions such as displaying the image preview or sending the file to the server using AJAX
        handlePipelineDecompositionFromImage();
    });
});

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

let lastDoneTask = 'pipeline_decomposition';
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
        chatContent = `<p></p><div class="sui-a-avatar as--you">\n<Icon name="user" />\n</div>`;
    } else {
        chatContent = `<span>\n<img class="avatar" src="static/saagie_avatar.svg">\n</span><p></p>`;
    }
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}

const createChatLi1010 = (message, className, imageUrl = null) => {
    // Create a chat <li> element with passed message, className, and optional imageUrl
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);

    // Create the chat content based on the provided parameters
    let chatContent = '';
    if (className === "outgoing") {
        // Outgoing message with user avatar
        chatContent = `<p>${message}<br><img src="${imageUrl}" alt="Uploaded Image"</p><div class="sui-a-avatar as--you">\n<Icon name="user" />\n</div>`;
    } else {
        // Incoming message with Saagie avatar
        chatContent = `<div class="sui-a-avatar">\n<img class="avatar" src="static/saagie_avatar.svg">\n</div><p>${message}</p>`;
    }

    // Append an image if imageUrl is provided
    //if (imageUrl) {
    //    chatContent += `<img src="${imageUrl}" alt="Uploaded Image">`;
    //}

    // Set the chat content to the created <li> element
    chatLi.innerHTML = chatContent;

    // Return the chat <li> element
    return chatLi;
}


const generatePipelineDecomposition = async (chatElement, userMessage) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "pipeline_decomposition", "user_message": userMessage }),
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        } else if (data.generic_message) {
            messageText = `<div class="sui-a-text">${data.generic_message}\n</div>`

            // Set the response message from the server
            messageElement.innerHTML = messageText;

        } else if (data.jobs) {
            // Extract the desired fields from each dictionary
            const extractedFields = data.jobs.map(item => {
                return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n</div>`;
            });

            // Join the extracted fields into a single message
            messageText = extractedFields.join('\n');

            // Set the response message from the server
            messageElement.innerHTML = messageText;
            
            // Show the button after the response is generated
            genCodesBtn.style.display = "block";

            // Pipeline Decomposition task was done with success
            lastDoneTask = 'pipeline_decomposition';
            chatInput.placeholder = "Ask me here to modify the above Pipeline/Job.";
        }

        

    } catch (error) {
        messageElement.classList.add("error");
        //messageElement.textContent = "Oops! Something went wrong. Please try again.";        
        messageElement.textContent = error.message;        

    } finally {
        window.scrollBy(0, chatbox.scrollHeight);
    }
}

const generatePipelineDecompositionFromImage2 = async (chatElement, userMessage, file) => {
    const messageElement = chatElement.querySelector("p");
    const genCodesBtn = document.getElementById("gen-codes-btn"); // Assuming you have a button with this ID

    try {
        // Create FormData object to send both file and other data
        const formData = new FormData();
        formData.append('file', file);

        // Other data
        const data = {
            task: 'pipeline_decomposition', // Specify the task
            user_message: userMessage // Provide user message if needed
        };

        // Convert data to JSON and append to FormData
        for (let key in data) {
            formData.append(key, data[key]);
        }

        // Make a POST request to the Flask endpoint
        const response = await fetch('generate-response', {
            method: "POST",
            body: formData,
        });

        const responseData = await response.json();

        if (responseData.error) {
            throw new Error(responseData.error);
        } else if (responseData.generic_message) {
            messageText = `<div class="sui-a-text">${responseData.generic_message}\n</div>`

            // Set the response message from the server
            messageElement.innerHTML = messageText;

        } else if (responseData.jobs) {
            // Extract the desired fields from each dictionary
            const extractedFields = responseData.jobs.map(item => {
                return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n</div>`;
            });

            // Join the extracted fields into a single message
            messageText = extractedFields.join('\n');

            // Set the response message from the server
            messageElement.innerHTML = messageText;

            // Show the button after the response is generated
            genCodesBtn.style.display = "block";

            // Pipeline Decomposition task was done with success
            lastDoneTask = 'pipeline_decomposition';
            chatInput.placeholder = "Ask me here to modify the above Pipeline/Job.";
        }
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = error.message;
    } finally {
        window.scrollBy(0, chatbox.scrollHeight);
    }
}

const generatePipelineDecompositionFromImage = async (chatElement, userMessage, file) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Create FormData object to send both file and other data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('task', 'pipeline_decomposition');
        formData.append('user_message', userMessage);

        // Make a POST request to the Flask endpoint
        const response = await fetch('pipeline-decomposition-from-image', {
            method: "POST",
            body: formData,
            // Set Content-Type header explicitly
            //headers: {
            //    "Content-Type": "multipart/form-data"
            //}
        });

        const responseData = await response.json();

        if (responseData.error) {
            throw new Error(responseData.error);
        } else if (responseData.generic_message) {
            messageText = `<div class="sui-a-text">${responseData.generic_message}\n</div>`

            // Set the response message from the server
            messageElement.innerHTML = messageText;

        } else if (responseData.jobs) {
            // Extract the desired fields from each dictionary
            const extractedFields = responseData.jobs.map(item => {
                return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n</div>`;
            });

            // Join the extracted fields into a single message
            messageText = extractedFields.join('\n');

            // Set the response message from the server
            messageElement.innerHTML = messageText;

            // Show the button after the response is generated
            genCodesBtn.style.display = "block";

            // Pipeline Decomposition task was done with success
            lastDoneTask = 'pipeline_decomposition';
            chatInput.placeholder = "Ask me here to modify the above Pipeline/Job.";
        }
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = error.message;
    } finally {
        window.scrollBy(0, chatbox.scrollHeight);
    }
}


const generateFirstCodeGeneration = async (chatElement, userMessage) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "first_code_generation", "user_message": userMessage }),
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
    
        } else if (data.generic_message) {
            messageText = `<div class="sui-a-text">${data.generic_message}\n</div>`

            // Set the response message from the server
            messageElement.innerHTML = messageText;

            // Show the button for the API
            createInSaagieBtn.style.display = "block";

        } else if (data.jobs) {
            // Extract the desired fields from each dictionary
            const extractedFields = data.jobs.map(item => {
                return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n<pre><code class="python hljs">${item.code}</code></pre>`;
            });

            // Join the extracted fields into a single message
            messageText = extractedFields.join('\n');

            // Set the response message from the server
            messageElement.innerHTML = messageText;
            
            // Show the button after the response is generated
            createInSaagieBtn.style.display = "block";

            // First Code Generation task was done with success
            lastDoneTask = 'first_code_generation';
        }

        
    } catch (error) {
        messageElement.classList.add("error");
        //messageElement.textContent = "Oops! Something went wrong. Please try again.";        
        messageElement.textContent = error.message; 
        // Display the genCodesBtn if the Code Generation failed
        genCodesBtn.style.display = "block";
    } finally {
        window.scrollBy(0, chatbox.scrollHeight);
    }
}

const generateIterationOnCodeGeneration = async (chatElement, userMessage) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "iteration_on_code_generation", "user_message": userMessage }),
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);

        } else if (data.generic_message) {
            messageText = `<div class="sui-a-text">${data.generic_message}\n</div>`

            // Set the response message from the server
            messageElement.innerHTML = messageText;

            // Show the button for the API
            createInSaagieBtn.style.display = "block";

        } else if (data.jobs) {

            // Extract the desired fields from each dictionary
            const extractedFields = data.jobs.map(item => {
                return `<div class="sui-a-text as--ml">Job ${item.id} : ${item.name}</div>\n<div class="sui-a-text">Description: ${item.description}\nInput Resources: ${JSON.stringify(item.input_resources)}\nOutput Resources: ${JSON.stringify(item.output_resources)}\n\n<pre><code class="python hljs">${item.code}</code></pre>`;
            });

            // Join the extracted fields into a single message
            const messageText = extractedFields.join('\n');

            // Set the response message from the server
            messageElement.innerHTML = messageText;
            
            // Show the button for the API
            createInSaagieBtn.style.display = "block";

            // Code Generation task was done with success
            lastDoneTask = 'iteration_on_code_generation';
        }

    } catch (error) {
        messageElement.classList.add("error");
        //messageElement.textContent = "Oops! Something went wrong. Please try again.";        
        messageElement.textContent = error.message; 
        // Display the genCodesBtn if the Code Generation failed
        genCodesBtn.style.display = "block";
    } finally {
        window.scrollBy(0, chatbox.scrollHeight);
    }
}

const generateCreationInSaagie = async (chatElement) => {
    const messageElement = chatElement.querySelector("p");

    try {
        // Make a POST request to the Flask endpoint
        const response = await fetch('generate-response', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "task": "creation_in_saagie", "user_message": "" }),
        });
        
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        };

        // Extract the result content from data
        const messageText = `<div class="sui-a-text">${data.result}</div>`;

        // Set the response message from the server
        messageElement.innerHTML = messageText;

        // Creation in Saagie task was done with success
        lastDoneTask = 'creation_in_saagie';

    } catch (error) {
        messageElement.classList.add("error");
        //messageElement.textContent = "Oops! Something went wrong. Please try again.";        
        messageElement.textContent = error.message; 
        // Display the createInSaagieBtn if the creation in Saagie failed
        createInSaagieBtn.style.display = "block";
    } finally {
        window.scrollBy(0, chatbox.scrollHeight);
    }
}

const handlePipelineDecomposition = async () => {
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

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    window.scrollBy(0, chatbox.scrollHeight);

    
    // Generate the response
    await generatePipelineDecomposition(incomingChatLi, userMessage);

}

const handlePipelineDecompositionFromImage0101 = async () => {
    // Hide all buttons
    buttonsInChatbox.forEach(button => {
        button.style.display = "none";
    });

    // Get the uploaded file
    const fileUpload = document.getElementById("file-upload");
    const uploadedFile = fileUpload.files[0];
    if (!uploadedFile) {
        console.error("No file uploaded");
        return;
    }

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the file name to the chatbox
    const fileNameMessage = `Uploaded Image: ${uploadedFile.name}`;
    const outgoingChatLi = createChatLi(fileNameMessage, "outgoing");
    chatbox.appendChild(outgoingChatLi);

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    window.scrollBy(0, chatbox.scrollHeight);

    // Generate the response from the uploaded image
    await generatePipelineDecompositionFromImage(incomingChatLi, fileNameMessage, uploadedFile);
}

const handlePipelineDecompositionFromImage = async () => {
    // Hide all buttons
    buttonsInChatbox.forEach(button => {
        button.style.display = "none";
    });

    // Get the uploaded file
    const fileUpload = document.getElementById("file-upload");
    const uploadedFile = fileUpload.files[0];
    if (!uploadedFile) {
        console.error("No file uploaded");
        return;
    }

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the file name to the chatbox
    const fileNameMessage = `Uploaded Image: ${uploadedFile.name}`;
    const outgoingChatLi = createChatLi1010(fileNameMessage, "outgoing", URL.createObjectURL(uploadedFile) );
    chatbox.appendChild(outgoingChatLi);

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    window.scrollBy(0, chatbox.scrollHeight);

    // Generate the response from the uploaded image
    await generatePipelineDecompositionFromImage(incomingChatLi, fileNameMessage, uploadedFile);
}


const handleFirstCodeGeneration = async () => {

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

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    window.scrollBy(0, chatbox.scrollHeight);
    
    // Generate the response
    await generateFirstCodeGeneration(incomingChatLi, userMessage);
}

const handleIterationOnCodeGeneration = async () => {

    // Hide all buttons
    buttonsInChatbox.forEach(button => {
        button.style.display = "none";
    });
    userMessage = chatInput.value.trim();
    if (userMessage === "") {
        userMessage = "Generate the codes please";
    }

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    const outgoingChatLi = createChatLi(userMessage, "outgoing");
    chatbox.appendChild(outgoingChatLi);

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    window.scrollBy(0, chatbox.scrollHeight);
    
    // Generate the response
    await generateIterationOnCodeGeneration(incomingChatLi, userMessage);
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
    window.scrollBy(0, chatbox.scrollHeight);
    
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
        //handleChat();
        // Check the value of lastTask and call the appropriate function
        if (lastDoneTask === 'pipeline_decomposition' || lastDoneTask === 'creation_in_saagie') {
            handlePipelineDecomposition();
        } else if (lastDoneTask === 'first_code_generation' || lastDoneTask === 'iteration_on_code_generation') {
            handleIterationOnCodeGeneration();
        }
    }
});


sendChatBtn.addEventListener("click", () => {
    // Check the value of lastTask and call the appropriate function
    if (lastDoneTask === 'pipeline_decomposition' || lastDoneTask === 'creation_in_saagie') {
        handlePipelineDecomposition();
        } else if (lastDoneTask === 'first_code_generation' || lastDoneTask === 'iteration_on_code_generation') {
        handleIterationOnCodeGeneration();
    }
});


genCodesBtn.addEventListener("click", () => {
    handleFirstCodeGeneration();
});

createInSaagieBtn.addEventListener("click", () => {
    handleCreationInSaagie();
});

// Add event listener to the restart button
restartBtn.addEventListener("click", async () => {
    try {
        // Make a POST request to the Flask endpoint to restart the application
        const response = await fetch('restart', {
            method: 'POST'
        });
        
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // If the restart is successful, reload the page
        window.location.reload();
    } catch (error) {
        console.error('Error restarting the app:', error);
    }
});
