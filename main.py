import os
from dotenv import load_dotenv
from wordpress_client import WordPressClient
from ollama_client import OllamaClient, OllamaError
from category_matcher import CategoryMatcher
from utils import make_slug

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize clients
    wp_client = WordPressClient(
        base_url=os.getenv('WORDPRESS_URL'),
        username=os.getenv('WORDPRESS_USERNAME'),
        password=os.getenv('WORDPRESS_PASSWORD')
    )
    
    # Initialize Ollama client
    ollama_client = OllamaClient(
        model_name=os.getenv('OLLAMA_MODEL', 'llama3:latest'),
        base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    )
    
    # Initialize category matcher
    category_matcher = CategoryMatcher()
    
    try:
        # Get uncategorized posts
        posts = wp_client.get_uncategorized_posts()
        print(f"Found {len(posts)} uncategorized posts")
        
        for post in posts:
            try:
                print(f"\nProcessing post: {post['title']['rendered']}")
                
                # Get category suggestion from Ollama
                try:
                    suggested_category = ollama_client.get_category(post['content']['rendered'])
                    print(f"Suggested category: {suggested_category}")
                    
                    # Get existing categories
                    existing_categories = wp_client.get_all_categories()
                    
                    # Find best matching category
                    category_id, category_name = category_matcher.find_best_category(suggested_category, existing_categories)
                    
                    if category_id:
                        # Category found, update post
                        wp_client.update_post_category(post['id'], category_id)
                        print(f"Updated category '{category_name}' for post {post['id']}")
                    else:
                        # No matching category found, create new one
                        category_id = wp_client.create_category(suggested_category)
                        wp_client.update_post_category(post['id'], category_id)
                        print(f"Created and set new category '{suggested_category}' for post {post['id']}")
                        
                except OllamaError as e:
                    print(f"Error getting category from Ollama: {e}")
                    continue
                    
            except Exception as e:
                print(f"Error processing post {post['id']}: {e}")
                continue
                
    except Exception as e:
        print(f"Error in main process: {e}")
        raise

if __name__ == "__main__":
    main()

    