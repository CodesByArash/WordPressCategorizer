# WordPress Category Matcher

This project uses Ollama to automatically categorize WordPress posts based on their content.

## Prerequisites

- Docker and Docker Compose
- Git
- Access to a WordPress site
- Access to Ollama (local or server)

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd WordPressProject
```

2. Create `.env` file:
```bash
# WordPress Configuration
WORDPRESS_URL=https://your-wordpress-site.com/wp-json/wp/v2
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-password

# Ollama Configuration
OLLAMA_MODEL=llama3:latest
OLLAMA_BASE_URL=http://localhost:11434

# Transformer Configuration
TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

3. Run with Docker:
```bash
docker-compose up --build
```

## Project Structure

- `main.py`: Main application file
- `ollama_client.py`: Ollama client for model interaction
- `wordpress_client.py`: WordPress client for post and category management
- `category_matcher.py`: Category matching logic
- `utils.py`: Utility functions

## Configuration

### WordPress
- `WORDPRESS_URL`: WordPress API URL
- `WORDPRESS_USERNAME`: WordPress username
- `WORDPRESS_PASSWORD`: WordPress password

### Ollama
- `OLLAMA_MODEL`: Ollama model name (default: llama3:latest)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)

### Transformer
- `TRANSFORMER_MODEL`: Sentence Transformer model name (default: all-MiniLM-L6-v2)

## How It Works

1. Connects to WordPress
2. Finds uncategorized posts
3. Uses Ollama to suggest categories
4. Uses Sentence Transformer to match with existing categories
5. Updates posts with appropriate categories

## Important Notes

- `.env` file is in `.gitignore` and should not be committed to the repository
- Use strong passwords for security
- Ensure Ollama server is accessible
- Required models will be downloaded on first run

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running
- Check `OLLAMA_BASE_URL` setting
- Port 11434 should be accessible

### WordPress Issues
- Verify WordPress credentials
- Ensure WordPress API is enabled
- Check `WORDPRESS_URL` setting

### Model Issues
- Verify Ollama model is installed
- Ensure sufficient disk space for model downloads
- Check internet connection

## Contributing

To contribute to the project:
1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Create a pull request

## License

MIT License 