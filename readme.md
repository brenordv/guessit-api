# GuessIt API

A RESTful API wrapper for the [GuessIt](https://github.com/guessit-io/guessit) library, which extracts information from video filenames.

## What is GuessIt API?

GuessIt API provides a simple HTTP interface to the powerful GuessIt library, allowing you to extract structured information from movie and TV show filenames. It's perfect for:

- Media centers and media management applications
- Metadata scrapers and organizers
- Any application that needs to parse media filenames

The API analyzes filenames and returns structured data including title, year, season, episode, quality, codec information, and more.

## How It Works

The application is built with FastAPI and exposes the GuessIt library's functionality through a RESTful API. It provides two main endpoints:

- `/api/guess` - Analyzes a filename and returns structured information
- `/api/health` - Provides a health check to verify the API is functioning correctly

## Installation and Usage

### Local Installation

#### Prerequisites
- Python 3.11 or higher

#### Using Virtual Environment (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/guessit-api.git
cd guessit-api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The API will be available at http://localhost:8000

#### Without Virtual Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/guessit-api.git
cd guessit-api

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Using Docker

#### Building the Docker Image

```bash
# On Linux/macOS:
./build-image.sh

# On Windows (PowerShell):
docker build -t guessit-api:latest .
```

#### Running the Docker Container

```bash
# On Linux/macOS:
./run-image.sh

# On Windows (PowerShell):
docker run -d --name guessit-api -p 10147:10147 --restart unless-stopped guessit-api:latest
```

The API will be available at http://localhost:10147

## API Usage Examples

### Analyzing a Movie Filename

```
GET /api/guess?it=Shin%20Godzilla%20(2016)%201080p%20Hybrid%20Bluray%20REMUX%20AVC%20Dual%20DTS-HD%20MA%203.1
```

Response:
```json
{
  "title": "Shin Godzilla",
  "year": 2016,
  "screen_size": "1080p",
  "source": "Blu-ray",
  "other": "Hybrid, Remux",
  "video_codec": "H.264",
  "audio_channels": "3.1",
  "audio_codec": "DTS-HD"
}
```

### Analyzing a TV Show Filename

```
GET /api/guess?it=Rick.and.Morty.S07E10.Fear.No.Mort.1080p.HMAX.WEB-DL.DDP5.1.H.264-FLUX.mkv
```

Response:
```json
{
  "title": "Rick and Morty",
  "season": 7,
  "episode": 10,
  "episode_title": "Fear No Mort",
  "screen_size": "1080p",
  "streaming_service": "HBO Max",
  "source": "Web",
  "audio_codec": "Dolby Digital Plus",
  "audio_channels": "5.1",
  "video_codec": "H.264",
  "release_group": "FLUX",
  "container": "mkv"
}
```

### Health Check

```
GET /api/health
```

Response:
```json
{
  "message": "healthy"
}
```

## More Examples

See the [example_requests.http](example_requests.http) file for more usage examples.

## Dependencies

This project relies on:
- [GuessIt](https://github.com/guessit-io/guessit) - The core library for parsing filenames
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Uvicorn](https://www.uvicorn.org/) - ASGI server for running the application
- [Requests](https://requests.readthedocs.io/) - HTTP library for testing

## License

This project is licensed under the [GNU Lesser General Public License v3 (LGPLv3)](https://www.gnu.org/licenses/lgpl-3.0.html), the same license as the GuessIt library.

## Acknowledgements

This project is a simple wrapper around the excellent [GuessIt](https://github.com/guessit-io/guessit) library. 
All the hard work of parsing and analyzing filenames is done by GuessIt, and that project is absolutely awesome! So go check it out! :D 