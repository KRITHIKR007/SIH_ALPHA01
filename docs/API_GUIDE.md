# 📚 DyslexiaCare API Documentation

## Base Configuration
- **Base URL**: `http://localhost:8000`
- **Content Types**: `application/json`, `multipart/form-data`
- **Authentication**: Bearer token for admin endpoints

## 🏥 Health & Status Endpoints

### GET /health
**Purpose**: Check API health status
```http
GET /health
```
**Response**:
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /
**Purpose**: Root endpoint with basic info
```http
GET /
```
**Response**:
```json
{
    "message": "Dyslexia Screening API is running",
    "status": "healthy"
}
```

## 📊 Dyslexia Screening

### POST /check_dyslexia
**Purpose**: Comprehensive dyslexia analysis using multiple input types

**Headers**:
```http
Content-Type: multipart/form-data
```

**Parameters** (all optional, but at least one required):
- `text`: string - Text sample for analysis
- `audio_file`: file - Audio recording (.wav, .mp3, .m4a)
- `handwriting_image`: file - Handwriting image (.png, .jpg, .jpeg)

**Example Request** (using curl):
```bash
curl -X POST "http://localhost:8000/check_dyslexia" \
  -F "text=The quick brown fox jumps over the lazy dog" \
  -F "audio_file=@reading_sample.wav" \
  -F "handwriting_image=@handwriting.jpg"
```

**Success Response** (200):
```json
{
    "session_id": "123",
    "confidence_score": 0.65,
    "analysis": {
        "text_analysis": {
            "word_count": 9,
            "average_word_length": 4.2,
            "complex_words_count": 1,
            "reversals_detected": [
                {
                    "detected": "saw",
                    "should_be": "was",
                    "type": "word"
                }
            ],
            "spelling_patterns": [],
            "confidence": 0.7,
            "recommendations": [
                "Consider visual processing exercises for letter reversals"
            ]
        },
        "speech_analysis": {
            "transcribed_text": "The quick brown fox jumps over the lazy dog",
            "reading_speed_wpm": 95,
            "audio_duration": 5.7,
            "accuracy_score": 0.98,
            "confidence": 0.6,
            "recommendations": [
                "Practice reading fluency exercises"
            ]
        },
        "ocr_analysis": {
            "extracted_text": "The quick brown fox",
            "text_confidence": 0.92,
            "letter_reversals": ["Potential reversal in: quick"],
            "writing_clarity_score": 0.85,
            "confidence": 0.8,
            "recommendations": [
                "Practice letter formation exercises"
            ]
        }
    },
    "recommendations": [
        "Consider consultation with a learning specialist",
        "Implement multi-sensory learning approaches",
        "Practice reading fluency exercises",
        "Use tactile letter formation activities",
        "Consider assistive technology tools",
        "Break complex tasks into smaller steps"
    ],
    "screening_summary": "Screening indicates medium likelihood of dyslexia indicators (confidence: 0.65)"
}
```

**Error Responses**:
- `400`: Missing input data
- `500`: Analysis processing failed

## 🔊 Text-to-Speech

### POST /tts
**Purpose**: Generate accessibility-focused text-to-speech audio

**Headers**:
```http
Content-Type: application/json
```

**Request Body**:
```json
{
    "text": "Hello world, this is a test of text-to-speech generation.",
    "speed": 1.0,
    "phonics_mode": false,
    "language": "en"
}
```

**Parameters**:
- `text`: string (required) - Text to convert to speech
- `speed`: float (optional, default: 1.0) - Speed multiplier (0.5-2.0)
- `phonics_mode`: boolean (optional, default: false) - Enable phonics processing
- `language`: string (optional, default: "en") - Language code

**Example Request**:
```bash
curl -X POST "http://localhost:8000/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "speed": 0.8,
    "phonics_mode": true,
    "language": "en"
  }'
```

**Success Response** (200):
```json
{
    "audio_file_path": "outputs/tts_1642234567.wav",
    "duration": 3.2,
    "settings_used": {
        "speed": 0.8,
        "phonics_mode": true,
        "language": "en"
    }
}
```

**Error Responses**:
- `400`: Invalid parameters
- `500`: TTS generation failed

## 🛡️ Admin Endpoints

All admin endpoints require Bearer token authentication:
```http
Authorization: Bearer hackathon-admin-2024
```

### GET /admin/stats
**Purpose**: Get platform usage statistics

**Example Request**:
```bash
curl -X GET "http://localhost:8000/admin/stats" \
  -H "Authorization: Bearer hackathon-admin-2024"
```

**Success Response** (200):
```json
{
    "total_sessions": 45,
    "average_confidence_score": 0.62,
    "sessions_today": 12
}
```

### GET /admin/sessions
**Purpose**: Retrieve analysis session history

**Query Parameters**:
- `limit`: int (optional, default: 100) - Maximum sessions to return

**Example Request**:
```bash
curl -X GET "http://localhost:8000/admin/sessions?limit=10" \
  -H "Authorization: Bearer hackathon-admin-2024"
```

**Success Response** (200):
```json
{
    "sessions": [
        {
            "id": 123,
            "timestamp": "2024-01-15T10:30:00Z",
            "input_data": {
                "text": "Sample text",
                "audio_file": null,
                "image_file": null
            },
            "analysis_result": { /* analysis data */ },
            "confidence_score": 0.65,
            "recommendations": ["recommendation1", "recommendation2"]
        }
    ],
    "total": 1
}
```

### DELETE /admin/clear
**Purpose**: Clear all analysis sessions

**Query Parameters**:
- `confirm`: boolean (required: true) - Confirmation flag

**Example Request**:
```bash
curl -X DELETE "http://localhost:8000/admin/clear?confirm=true" \
  -H "Authorization: Bearer hackathon-admin-2024"
```

**Success Response** (200):
```json
{
    "message": "Cleared 45 sessions"
}
```

**Error Responses**:
- `400`: Missing confirmation
- `403`: Invalid admin token

## 📝 Postman Collection

### Import Collection
Create a new Postman collection with the following requests:

1. **Health Check**
   - Method: GET
   - URL: `{{base_url}}/health`

2. **Dyslexia Analysis - Text Only**
   - Method: POST
   - URL: `{{base_url}}/check_dyslexia`
   - Body: form-data
     - Key: `text`, Value: `"The quick brown fox jumps over the lazy dog"`

3. **Dyslexia Analysis - Multimodal**
   - Method: POST
   - URL: `{{base_url}}/check_dyslexia`
   - Body: form-data
     - Key: `text`, Value: `"Sample text"`
     - Key: `audio_file`, Type: File
     - Key: `handwriting_image`, Type: File

4. **Text-to-Speech**
   - Method: POST
   - URL: `{{base_url}}/tts`
   - Headers: `Content-Type: application/json`
   - Body: raw (JSON)
     ```json
     {
       "text": "Hello world",
       "speed": 1.0,
       "phonics_mode": false,
       "language": "en"
     }
     ```

5. **Admin Stats**
   - Method: GET
   - URL: `{{base_url}}/admin/stats`
   - Headers: `Authorization: Bearer {{admin_token}}`

### Environment Variables
Create a Postman environment with:
- `base_url`: `http://localhost:8000`
- `admin_token`: `hackathon-admin-2024`

## 🔧 Testing Scripts

### Python Test Script
```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
ADMIN_TOKEN = "hackathon-admin-2024"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Health check passed")

def test_dyslexia_analysis():
    data = {"text": "The quick brown fox jumps over the lazy dog"}
    response = requests.post(f"{BASE_URL}/check_dyslexia", data=data)
    assert response.status_code == 200
    result = response.json()
    assert "confidence_score" in result
    print("✅ Dyslexia analysis passed")

def test_tts():
    payload = {
        "text": "Hello world",
        "speed": 1.0,
        "phonics_mode": False,
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/tts", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "audio_file_path" in result
    print("✅ TTS generation passed")

def test_admin_stats():
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    response = requests.get(f"{BASE_URL}/admin/stats", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "total_sessions" in result
    print("✅ Admin stats passed")

if __name__ == "__main__":
    test_health()
    test_dyslexia_analysis()
    test_tts()
    test_admin_stats()
    print("🎉 All tests passed!")
```

## 🚀 Development Tips

### Local Testing Setup
1. Start backend: `cd backend && python -m uvicorn main:app --reload`
2. Test endpoints with Postman or curl
3. Check logs in console for debugging
4. Use admin panel to monitor sessions

### File Upload Testing
For file upload endpoints, prepare test files:
- **Audio**: WAV/MP3 files under 50MB
- **Images**: Clear handwriting samples in PNG/JPG format
- **Text**: Sample reading passages with potential dyslexia indicators

### Error Debugging
Common issues and solutions:
- **500 errors**: Check backend logs for AI model initialization
- **Timeout errors**: Reduce file sizes or increase timeout settings
- **Permission errors**: Ensure upload/output directories exist
- **Token errors**: Verify admin token in headers

### Performance Optimization
- Use smaller audio files (< 10MB) for faster processing
- Compress images while maintaining readability
- Test with realistic data sizes for demo scenarios
- Monitor response times for user experience optimization