# YouTube Transcript API

A FastAPI-based service that retrieves transcripts from YouTube videos.

## Features

- Retrieve transcripts from any YouTube video using its video ID
- Optional proxy support for accessing YouTube in restricted regions
- Simple REST API interface
- Error handling for invalid video IDs or unavailable transcripts

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-transcriber.git
cd youtube-transcriber
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at `http://localhost:8000`

### API Endpoints

#### GET /transcript

Retrieves the transcript for a YouTube video.

**Parameters:**
- `video_id` (required): The YouTube video ID
- `proxy_username` (optional): Proxy username
- `proxy_password` (optional): Proxy password
- `proxy_host` (optional): Proxy host address
- `proxy_port` (optional): Proxy port number

**Example Request:**
```bash
# Without proxy
curl "http://localhost:8000/transcript?video_id=VIDEO_ID"

# With proxy
curl "http://localhost:8000/transcript?video_id=VIDEO_ID&proxy_username=USER&proxy_password=PASS&proxy_host=HOST&proxy_port=PORT"
```

**Example Response:**
```json
{
    "video_id": "VIDEO_ID",
    "transcript": "Full transcript text here..."
}
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (invalid video ID or transcript not available)
- 500: Internal Server Error

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
