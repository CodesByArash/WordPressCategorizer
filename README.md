# WordPress Category Matcher

This project uses Ollama to automatically categorize WordPress posts based on their content.

## Prerequisites

- Docker and Docker Compose
- Git

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd WordPressProject
```

2. Create a `.env` file with your WordPress credentials:
```bash
WORDPRESS_URL=your-wordpress-site-url
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-password
```

3. Build and start the containers:
```bash
docker-compose up --build
```

## Usage

The application will:
1. Connect to your WordPress site
2. Use Ollama to analyze post content
3. Suggest appropriate categories
4. Update posts with the suggested categories

## Development

- The main application code is in `main.py`
- Ollama client code is in `ollama_client.py`
- WordPress client code is in `wordpress_client.py`
- Category matching logic is in `category_matcher.py`
- Utility functions are in `utils.py`

## Docker Commands

- Start the application: `docker-compose up`
- Start in background: `docker-compose up -d`
- Stop the application: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild containers: `docker-compose up --build`

## Notes

- The Ollama model (llama3:latest) will be downloaded automatically on first run
- Make sure your WordPress site is accessible from the container
- The application uses the Ollama API to generate category suggestions 