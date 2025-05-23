from wordpress_client import WordPressClient
from category_matcher import CategoryMatcher
from ollama_client import get_category_from_ollama

USERNAME = "asimir"
PASSWORD = "ZSbd jn8P MewQ Rihf LYjQ L0Jp"
BASE_URL = "https://cms111.s4-tastewp.com/wp-json/wp/v2"

wp_client = WordPressClient(BASE_URL, USERNAME, PASSWORD)
category_matcher = CategoryMatcher()

def main():
    try:
        all_cats = wp_client.get_all_categories()
        uncategorized_posts = wp_client.get_uncategorized_posts()
        print("posts got")
        for post in uncategorized_posts:
            post_id = post['id']
            content = post['content']['rendered']
            suggested = get_category_from_ollama(content)

            matched_id, matched_name = category_matcher.find_best_category(suggested, all_cats)

            if matched_id:
                print(f"Matched category: {matched_name}")
                wp_client.update_post_category(post_id, matched_id)
            else:
                print(f"Creating new category: {suggested}")
                new_cat_id = wp_client.create_category(suggested)
                wp_client.update_post_category(post_id, new_cat_id)
                all_cats = wp_client.get_all_categories()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting script ...")
    main()

    