import os
from dotenv import load_dotenv
from wordpress_client import WordPressClient
from ollama_client import OllamaClient, OllamaError
from category_matcher import CategoryMatcher
from utils import create_slug

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize clients
    wp_client = WordPressClient(
        url=os.getenv('WORDPRESS_URL'),
        username=os.getenv('WORDPRESS_USERNAME'),
        password=os.getenv('WORDPRESS_PASSWORD')
    )
    
    # Initialize Ollama client with environment variables
    ollama_client = OllamaClient(
        model_name=os.getenv('OLLAMA_MODEL', 'llama3:latest'),
        base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    )
    
    print(f"Using Ollama model: {ollama_client.model_name}")
    print(f"Using Ollama server: {ollama_client.base_url}")
    
    category_matcher = CategoryMatcher()
    
    try:
        # Get all posts
        posts = wp_client.get_all_posts()
        print(f"Found {len(posts)} posts to process")
        
        for post in posts:
            try:
                print(f"\nProcessing post: {post.title}")
                
                # Get current categories
                current_categories = [cat['name'] for cat in post.categories]
                print(f"Current categories: {', '.join(current_categories)}")
                
                # Get category suggestion from Ollama
                try:
                    suggested_category = ollama_client.get_category(post.content)
                    print(f"Suggested category: {suggested_category}")
                    
                    # Find or create the category
                    category_id = category_matcher.find_or_create_category(suggested_category)
                    
                    # Update post categories
                    if category_id not in post.categories:
                        new_categories = post.categories + [category_id]
                        wp_client.update_post_categories(post.id, new_categories)
                        print(f"Updated categories for post {post.id}")
                    else:
                        print(f"Category already exists for post {post.id}")
                        
                except OllamaError as e:
                    print(f"Error getting category from Ollama: {e}")
                    continue
                    
            except Exception as e:
                print(f"Error processing post {post.id}: {e}")
                continue
                
    except Exception as e:
        print(f"Error in main process: {e}")
        raise

if __name__ == "__main__":
    main()

    