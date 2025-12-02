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
let riskChart = null;
let chartDependenciesRegistered = false;

const riskChartCenterTextPlugin = {
    id: 'riskChartCenterTextPlugin',
    afterDraw(chart) {
        const centerText = chart.config?.options?.plugins?.centerText;
        if (!centerText) return;

        const meta = chart.getDatasetMeta(0);
        if (!meta || !meta.data || !meta.data.length) return;

        const centerPoint = meta.data[0].getProps(['x', 'y'], true);
        const { ctx } = chart;

        ctx.save();
        ctx.fillStyle = centerText.color || '#333';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        ctx.font = `${centerText.fontWeight || 600} ${centerText.fontSize || 26}px ${centerText.fontFamily || 'Poppins'}`;
        ctx.fillText(centerText.text || '', centerPoint.x, centerPoint.y - 10);

        if (centerText.subtext) {
            ctx.font = `${centerText.subFontWeight || 500} ${centerText.subFontSize || 13}px ${centerText.fontFamily || 'Poppins'}`;
            ctx.fillText(centerText.subtext, centerPoint.x, centerPoint.y + 16);
        }

        ctx.restore();
    }
};

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

        // Reset conversation history for the new assessment
        conversationHistory = [];
        
        // Display results with minimal information, let AI agent provide detailed recommendations
        displayResults(result);
        
        // Add result to chat with context-aware message to get detailed recommendations
        addBotMessage(`I've analyzed the patient data. The dengue risk is ${Math.round(result.probability * 100)}% (${result.risk_level} risk). Let me provide you with detailed, personalized recommendations based on this assessment. What would you like to know first?`);
        
        // Automatically ask AI agent for detailed recommendations
        setTimeout(() => {
            requestDetailedRecommendations();
        }, 1000);
        
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

// Request detailed recommendations from AI agent
async function requestDetailedRecommendations() {
    if (!currentRiskAssessment) return;
    
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
        // Send request to AI agent for detailed recommendations
        const chatPayload = {
            message: "Please provide detailed recommendations for this dengue risk assessment including diet, lifestyle, prevention measures, and when to seek medical help.",
            conversation_history: conversationHistory,
            risk_assessment: currentRiskAssessment,
            include_full_recommendations: true
        };
        
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
        conversationHistory = data.conversation_history || [];
        
        // Add bot response to chat
        addBotMessage(data.response);
        
    } catch (error) {
        // Remove typing indicator
        typingIndicator.remove();
        
        console.error('Chat error:', error);
        addBotMessage("Sorry, I encountered an error while generating detailed recommendations. Please try asking me directly.");
    }
}

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
                conversation_history: conversationHistory,
            };
            
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
            conversationHistory = data.conversation_history || [];
            
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
    
    // Convert markdown bold syntax to HTML bold tags
    const formattedMessage = message
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Convert **text** to <strong>text</strong>
        .replace(/\n/g, '<br>');  // Convert newlines to <br> tags
    
    messageElement.innerHTML = `
        <div class="avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p>${formattedMessage}</p>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function ensureChartRegistration() {
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js is not available. Skipping chart rendering.');
        return false;
    }

    if (!chartDependenciesRegistered) {
        if (Array.isArray(Chart.registerables)) {
            Chart.register(...Chart.registerables);
        }
        chartDependenciesRegistered = true;
    }

    return true;
}

function getRiskColor(riskLevel) {
    switch ((riskLevel || '').toLowerCase()) {
        case 'high':
            return '#f44336';
        case 'medium':
            return '#ff9800';
        case 'low':
            return '#4caf50';
        default:
            return '#2196f3';
    }
}

function getRiskLabel(riskLevel) {
    return riskLevel ? `${riskLevel} Risk` : 'Risk Level';
}

function renderRiskChart(probability, riskLevel) {
    if (!ensureChartRegistration()) {
        return;
    }

    const canvas = document.getElementById('risk-chart');
    if (!canvas) {
        return;
    }

    const riskPercent = Math.round(Math.min(Math.max(probability * 100, 0), 100));
    const remaining = Math.max(0, 100 - riskPercent);
    const color = getRiskColor(riskLevel);

    if (riskChart) {
        riskChart.destroy();
        riskChart = null;
    }

    riskChart = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Risk Probability', 'Remaining'],
            datasets: [{
                data: [riskPercent, remaining],
                backgroundColor: [color, '#e3e7eb'],
                hoverBackgroundColor: [color, '#d4d9dd'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            layout: {
                padding: 10
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label(context) {
                            return `${context.label}: ${context.parsed}%`;
                        }
                    }
                },
                centerText: {
                    text: `${riskPercent}%`,
                    subtext: getRiskLabel(riskLevel),
                    color,
                    fontFamily: 'Poppins',
                    fontSize: 28,
                    fontWeight: 700,
                    subFontSize: 14,
                    subFontWeight: 500
                }
            }
        },
        plugins: [riskChartCenterTextPlugin]
    });
}

function displayResults(result) {
    const riskLevel = result.risk_level || 'Unknown';
    const riskClass = riskLevel.toLowerCase();
    const riskColor = getRiskColor(riskLevel);
    
    resultsContainer.innerHTML = `
        <div class="risk-result">
            <div class="risk-badge ${riskClass}">
                ${riskLevel.toUpperCase()} RISK
            </div>
            <div class="risk-percentage" style="color: ${riskColor}">
                ${Math.round(result.probability * 100)}%
            </div>
            <div class="risk-description">
                <p>Based on the patient profile and location data, the calculated dengue risk probability is <strong>${Math.round(result.probability * 100)}%</strong>.</p>
            </div>
            <div class="risk-chart-container">
                <canvas id="risk-chart"></canvas>
            </div>
            
            <div class="recommendations">
                <h3><i class="fas fa-lightbulb"></i> Recommendations</h3>
                <div class="recommendation-content">
                    <p>For detailed, personalized recommendations, please consult with the AI assistant. 
                    The AI will provide specific guidance based on your risk level, patient profile, 
                    and location context.</p>
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

    renderRiskChart(result.probability, result.risk_level);
}

// Initialize with a welcome message
document.addEventListener('DOMContentLoaded', function() {
    addBotMessage("Hello! I'm your Dengue Intelligence Assistant. Enter patient information in the form to get started with risk assessment, and I'll provide detailed, personalized recommendations based on the AI analysis.");
    console.log('Dengue Risk Predictor frontend initialized');
});