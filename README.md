# WordPress Category Matcher

This project uses Ollama to automatically categorize WordPress posts based on their content. It analyzes post content using AI to suggest appropriate categories and matches them with existing WordPress categories.

## Prerequisites

- Python 3.11 or higher
- Ollama (local installation)
- Access to a WordPress site with API access
- Sufficient disk space (at least 2GB) for models

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd WordPressProject
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
# source venv/bin/activate
```

3. Install required packages:
```bash
# This will also install PyTorch automatically
# The installation might take a few minutes
pip install -r requirements.txt
```

4. Install Ollama:
   - Download and install from [Ollama's website](https://ollama.com)
   - Start Ollama server in a separate terminal:
```bash
ollama serve
```

5. Download the required Ollama model:
```bash
ollama pull llama2:latest
```

6. Create `.env` file in the project root:
```env
# WordPress Configuration
WORDPRESS_URL=https://your-wordpress-site.com/wp-json/wp/v2
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-password

# Ollama Configuration
OLLAMA_MODEL=llama2:latest
OLLAMA_BASE_URL=http://localhost:11434

# Transformer Configuration
TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

## Running the Application

1. Make sure Ollama server is running:
```bash
ollama serve
```

2. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application file that orchestrates the category matching process
- `ollama_client.py`: Handles communication with Ollama for AI-powered category suggestions
- `wordpress_client.py`: Manages WordPress API interactions for posts and categories
- `category_matcher.py`: Implements category matching logic using sentence transformers
- `utils.py`: Utility functions for common operations

## Configuration

### WordPress Settings
- `WORDPRESS_URL`: Your WordPress REST API URL (e.g., https://example.com/wp-json/wp/v2)
- `WORDPRESS_USERNAME`: WordPress username
- `WORDPRESS_PASSWORD`: WordPress application password

### Ollama Settings
- `OLLAMA_MODEL`: Ollama model to use (default: llama2:latest)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)

### Transformer Settings
- `TRANSFORMER_MODEL`: Sentence Transformer model for semantic matching (default: all-MiniLM-L6-v2)

## How It Works

1. Connects to WordPress and finds uncategorized posts
2. Uses Ollama to analyze post content and suggest appropriate categories
3. Uses Sentence Transformer to find the best matching existing category
4. Updates posts with the matched or newly created categories

## Troubleshooting

### Ollama Issues
- Ensure Ollama is running (`ollama serve`)
- Verify model is installed (`ollama list`)
- Check if port 11434 is accessible
- Try pulling the model again if needed (`ollama pull llama2:latest`)

### WordPress Issues
- Verify WordPress credentials
- Ensure WordPress REST API is enabled
- Check if the API URL is correct
- Verify you have proper permissions

### Python/Environment Issues
- Make sure you're using Python 3.11 or higher
- Verify virtual environment is activated
- Check if all requirements are installed
- Ensure you have sufficient disk space

### Installation Issues
- The installation of `sentence-transformers` might take several minutes as it includes PyTorch
- Ensure you have a stable internet connection during installation
- If PyTorch installation fails, try installing it separately first:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## Security Notes

- Never commit `.env` file to version control
- Use strong passwords for WordPress
- Keep your Ollama installation updated
- Use application passwords for WordPress API access
- Never hardcode credentials in the source code
- Regularly rotate your WordPress application passwords
- Use HTTPS for WordPress API URL
- Keep your Python packages updated for security patches
- Consider using a password manager to manage your credentials
- If you accidentally commit sensitive information, immediately rotate all affected credentials

### Environment Variables Security
- Store all sensitive information in `.env` file
- Keep `.env` file in `.gitignore`
- Use different credentials for development and production
- Never share your `.env` file
- Regularly audit your `.env` file for unnecessary variables
- Use strong, unique passwords for each environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

MIT License 