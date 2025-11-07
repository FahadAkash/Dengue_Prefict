# Dengue Risk Predictor Frontend

A beautiful, responsive web interface for the Dengue Risk Prediction System.

## Features

- Modern, responsive UI with gradient designs
- Patient information input form
- Real-time risk assessment visualization
- AI-powered chat assistant
- Location-based risk analysis
- Test result interpretation
- Personalized recommendations

## How to Run

1. **Start the server:**
   ```bash
   python server.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:8000`

## File Structure

- `index.html` - Main HTML structure
- `style.css` - Styling and responsive design
- `script.js` - Frontend JavaScript functionality
- `server.py` - Simple HTTP server with API endpoint

## API Endpoint

The frontend communicates with a backend API endpoint:

- **POST /predict** - Submit patient data for risk assessment

## Data Format

The API expects patient data in the following format:

```json
{
  "Age": 30,
  "Gender": 1,
  "NS1": 0,
  "IgG": 1,
  "IgM": 1,
  "Area": "Badda",
  "AreaType": "Urban",
  "HouseType": "Building",
  "District": "Dhaka"
}
```

## Test Results Interpretation

- **NS1 (0/1)**: Antigen test (Negative/Positive)
- **IgG (0/1)**: Antibody test (Negative/Positive)
- **IgM (0/1)**: Antibody test (Negative/Positive)

## Risk Levels

- **Low (0-39%)**: Minimal risk, routine monitoring
- **Medium (40-69%)**: Moderate risk, enhanced prevention
- **High (70-100%)**: High risk, immediate action required

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Responsive Design

The interface is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile devices

## Technologies Used

- HTML5
- CSS3 (Flexbox, Grid)
- JavaScript (ES6+)
- Python (HTTP Server)
- Font Awesome (Icons)
- Google Fonts (Poppins)

## Customization

To customize the interface:
1. Modify `style.css` for visual changes
2. Update `script.js` for functionality changes
3. Adjust `server.py` for backend integration

## Testing the API

You can test the API using the provided test script:

```bash
python test_api.py
```

This will send a sample request to the API and display the response.

## User Interface Overview

### Header Section
- Project title with virus icon
- Subtitle describing the system

### Input Form
- Age input (numeric)
- Gender selection (dropdown)
- Test results checkboxes (NS1, IgG, IgM)
- Area selection (dropdown with all Dhaka areas)
- District selection (currently Dhaka only)

### Results Display
- Risk level badge (color-coded)
- Probability percentage (large display)
- Risk description
- Personalized recommendations:
  - Immediate actions
  - Prevention measures
  - Medical advice
  - Location context

### AI Assistant
- Chat interface with message history
- User input field with send button
- Bot responses with avatar icons
- Preloaded with helpful information

## Design Features

### Color Scheme
- Primary: Teal green (#00796b) for medical/trust theme
- Risk levels: Red (high), Orange (medium), Green (low)
- Background: Light gradient for modern look

### Typography
- Poppins font for clean, modern appearance
- Responsive text sizing for all devices

### Interactive Elements
- Hover effects on cards and buttons
- Smooth transitions and animations
- Loading states during API calls
- Error handling and display

### Responsive Layout
- Two-column layout on desktop
- Single column on mobile
- Flexible form elements
- Adaptive chat interface

## Future Enhancements

1. Integration with real ML model API
2. Multi-language support
3. Enhanced data visualization
4. Export functionality for reports
5. User authentication and history tracking
6. Mobile app version
7. Additional location support
8. Real-time data updates