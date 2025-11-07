// DOM Elements
const predictionForm = document.getElementById('prediction-form');
const resultsContainer = document.getElementById('results-container');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const districtSelect = document.getElementById('district');
const areaSelect = document.getElementById('area');

// Conversation history for chat
let conversationHistory = [];
let currentRiskAssessment = null;

// Area data by district (simplified for common areas)
const areasByDistrict = {
    "Dhaka": [
        "Adabor", "Badda", "Banasree", "Bangshal", "Biman Bandar", "Bosila", "Cantonment",
        "Chawkbazar", "Demra", "Dhanmondi", "Gendaria", "Gulshan", "Hazaribagh",
        "Jatrabari", "Kadamtali", "Kafrul", "Kalabagan", "Kamrangirchar", "Keraniganj",
        "Khilgaon", "Khilkhet", "Lalbagh", "Mirpur", "Mohammadpur", "Motijheel",
        "New Market", "Pallabi", "Paltan", "Ramna", "Rampura", "Sabujbagh",
        "Shahbagh", "Sher-e-Bangla Nagar", "Shyampur", "Sutrapur", "Tejgaon"
    ],
    "Chittagong": [
        "Agrabad", "Bakolia", "Bayezid Bostami", "Chandgaon", "Chawkbazar", 
        "Double Mooring", "EPZ", "Firozpur", "Golamari", "Halishahar",
        "Jalalabad", "Jubilee Road", "Karnaphuli", "Khulshi", "Lal Khan Bazar",
        "Lalkhan Bazar", "Madarbari", "Muradpur", "Nasirabad", "New Market",
        "Oxygen", "Pahartali", "Panchlaish", "Patenga", "Rampura TSO",
        "Raozan", "Sholoshahar", "Sikder Medical", "Sitakunda"
    ],
    "Khulna": [
        "Alamdanga", "Bagherpara", "Chalna", "Dacope", "Digholia", "Dumuria",
        "Harintana", "Khalishpur", "Khanjahanpur", "Khulna Sadar", "Labanchora",
        "Madaripur", "Paikgacha", "Phultala", "Rupsha", "Sonadanga", "Terokhada"
    ],
    "Rajshahi": [
        "Bagha", "Bagmara", "Charghat", "Durgapur", "Godagari", "Mohanpur",
        "Paba", "Putia", "Rajshahi Sadar", "Shah Mokdum", "Tanore"
    ],
    "Barisal": [
        "Agailjhara", "Babuganj", "Bakerganj", "Banaripara", "Barisal Sadar",
        "Gournadi", "Hizla", "Mehendiganj", "Muladi", "Wazirpur"
    ],
    "Sylhet": [
        "Balaganj", "Beanibazar", "Bishwanath", "Companiganj", "Dakshin Surma",
        "Fenchuganj", "Golapganj", "Gowainghat", "Jaintiapur", "Kanaighat",
        "Osmani Nagar", "Sylhet Sadar", "Zakiganj"
    ],
    "Rangpur": [
        "Badarganj", "Gangachara", "Kaunia", "Mithapukur", "Pirgacha",
        "Pirganj", "Rangpur Sadar", "Taraganj"
    ],
    "Mymensingh": [
        "Bhaluka", "Dhobaura", "Fulbaria", "Gaffargaon", "Gauripur",
        "Haluaghat", "Ishwarganj", "Muktagacha", "Mymensingh Sadar",
        "Nandail", "Phulpur", "Trishal"
    ]
};

// Initialize area options based on district selection
districtSelect.addEventListener('change', function() {
    const selectedDistrict = this.value;
    areaSelect.innerHTML = '<option value="">Select Area</option>';
    
    if (selectedDistrict && areasByDistrict[selectedDistrict]) {
        areasByDistrict[selectedDistrict].forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            areaSelect.appendChild(option);
        });
        areaSelect.disabled = false;
    } else {
        areaSelect.disabled = true;
    }
});

// Form Submission Handler
predictionForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(predictionForm);
    const data = {
        Age: parseInt(formData.get('age')),
        Gender: parseInt(formData.get('gender')),
        NS1: formData.get('ns1') ? 1 : 0,
        IgG: formData.get('igg') ? 1 : 0,
        IgM: formData.get('igm') ? 1 : 0,
        Area: formData.get('area'),
        AreaType: formData.get('area-type'),
        HouseType: formData.get('house-type'),
        District: formData.get('district')
    };
    
    // Validate required fields
    if (!data.District || !data.Area || !data.AreaType || !data.HouseType) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Show loading state
    resultsContainer.innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Analyzing risk factors...</p>
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
        </div>
    `;
    
    try {
        console.log('Sending prediction request with data:', data);
        
        // Call the frontend server which will forward to backend API
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        console.log('Received response from server:', response);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server error response:', errorText);
            
            if (response.status === 503) {
                throw new Error('Backend service unavailable. Please start the backend API server on port 8001.');
            } else {
                throw new Error(`Failed to get prediction: ${response.status} ${response.statusText} - ${errorText}`);
            }
        }
        
        const result = await response.json();
        console.log('Prediction result:', result);
        
        // Store current risk assessment for chat context
        currentRiskAssessment = {
            probability: result.probability,
            risk_level: result.risk_level,
            age: data.Age,
            gender: data.Gender === 1 ? "Male" : "Female",
            ns1: data.NS1 === 1 ? "Positive" : "Negative",
            igg: data.IgG === 1 ? "Positive" : "Negative",
            igm: data.IgM === 1 ? "Positive" : "Negative",
            area: data.Area,
            district: data.District
        };
        
        // Display results
        displayResults(result);
        
        // Add result to chat with context-aware message
        addBotMessage(`I've analyzed the patient data. The dengue risk is ${Math.round(result.probability * 100)}% (${result.risk_level} risk). I can provide detailed recommendations based on this assessment. What would you like to know?`);
        
    } catch (error) {
        console.error('Error during prediction:', error);
        resultsContainer.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error calculating risk: ${error.message}</p>
            </div>
        `;
    }
});

// Chat Functionality
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message typing-indicator';
        typingIndicator.innerHTML = `
            <div class="avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p><i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle"></i></p>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            // Send message to backend chat endpoint with risk assessment context
            const chatPayload = {
                message: message,
                conversation_history: conversationHistory
            };
            
            // Include risk assessment data if available
            if (currentRiskAssessment) {
                chatPayload.risk_assessment = currentRiskAssessment;
            }
            
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(chatPayload)
            });
            
            // Remove typing indicator
            typingIndicator.remove();
            
            if (!response.ok) {
                throw new Error(`Chat error: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            conversationHistory = data.conversation_history;
            
            // Add bot response to chat
            addBotMessage(data.response);
            
        } catch (error) {
            // Remove typing indicator
            typingIndicator.remove();
            
            console.error('Chat error:', error);
            addBotMessage("Sorry, I encountered an error while processing your request. Please try again.");
        }
    }
}

// Helper Functions
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message user-message';
    messageElement.innerHTML = `
        <div class="avatar">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    messageElement.innerHTML = `
        <div class="avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayResults(result) {
    const riskClass = result.risk_level.toLowerCase();
    const riskColor = riskClass === 'high' ? '#f44336' : riskClass === 'medium' ? '#ff9800' : '#4caf50';
    
    // Format the recommendation text
    let formattedRecommendation = result.recommendation;
    if (formattedRecommendation) {
        // Convert newlines to HTML breaks
        formattedRecommendation = formattedRecommendation.replace(/\n/g, '<br>');
    }
    
    resultsContainer.innerHTML = `
        <div class="risk-result">
            <div class="risk-badge ${riskClass}">
                ${result.risk_level.toUpperCase()} RISK
            </div>
            <div class="risk-percentage" style="color: ${riskColor}">
                ${Math.round(result.probability * 100)}%
            </div>
            <div class="risk-description">
                <p>Based on the patient profile and location data, the calculated dengue risk probability is <strong>${Math.round(result.probability * 100)}%</strong>.</p>
            </div>
            
            <div class="recommendations">
                <h3><i class="fas fa-lightbulb"></i> Recommendations</h3>
                <div class="recommendation-content">
                    ${formattedRecommendation || 'No specific recommendations available.'}
                </div>
            </div>
            
            ${result.key_factors ? `
            <div class="key-factors">
                <h3><i class="fas fa-key"></i> Key Factors</h3>
                <ul>
                    ${Object.entries(result.key_factors).map(([key, value]) => 
                        `<li><strong>${key.replace(/_/g, ' ')}:</strong> ${value}</li>`
                    ).join('')}
                </ul>
            </div>
            ` : ''}
        </div>
    `;
}

// Initialize with a welcome message
document.addEventListener('DOMContentLoaded', function() {
    addBotMessage("Hello! I'm your Dengue Intelligence Assistant. Enter patient information in the form to get started with risk assessment, or ask me anything about dengue prevention and treatment.");
    console.log('Dengue Risk Predictor frontend initialized');
});