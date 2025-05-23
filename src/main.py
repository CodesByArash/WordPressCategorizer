import os
from dotenv import load_dotenv
from wordpress_client import WordPressClient
from ollama_client import OllamaClient, OllamaError
from category_matcher import CategoryMatcher
from utils import make_slug

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')

    if not os.path.exists(env_path):
        print("Error: .env file not found!")
        print("Please create a .env file with your WordPress and Ollama settings.")
        return

    load_dotenv(env_path)
    
    wp_url = os.getenv('WORDPRESS_URL')
    wp_username = os.getenv('WORDPRESS_USERNAME')
    wp_password = os.getenv('WORDPRESS_PASSWORD')
    
    if not all([wp_url, wp_username, wp_password]):
        print("Error: Missing WordPress settings in .env file!")
        print("Please set WORDPRESS_URL, WORDPRESS_USERNAME, and WORDPRESS_PASSWORD")
        return    
    try:

        wp_client = WordPressClient(
            base_url=wp_url,
            username=wp_username,
            password=wp_password
        )
        
        ollama_client = OllamaClient(
            model_name=os.getenv('OLLAMA_MODEL', 'llama3:latest'),
            base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        )
        
        category_matcher = CategoryMatcher()


        posts = wp_client.get_uncategorized_posts()
        print(f"Found {len(posts)} uncategorized posts")
        
        for post in posts:
            try:
                print(f"\nProcessing post: {post['title']['rendered']}")
                
                try:
                    suggested_category = ollama_client.get_category(post['content']['rendered'])
                    print(f"Suggested category: {suggested_category}")
                    
                    existing_categories = wp_client.get_all_categories()
                    
                    category_id, category_name = category_matcher.find_best_category(suggested_category, existing_categories)
                    
                    if category_id:
                        wp_client.update_post_category(post['id'], category_id)
                        print(f"Updated category '{category_name}' for post {post['id']}")
                    else:
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

if __name__ == "__main__":
    main()

    