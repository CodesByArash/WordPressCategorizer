import requests
import base64
import json
import re
from sentence_transformers import SentenceTransformer, util
from utils import make_slug

class WordPressClient:
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize WordPress client with credentials
        
        Args:
            base_url (str): WordPress REST API base URL (e.g. https://example.com/wp-json/wp/v2)
            username (str): WordPress username
            password (str): WordPress application password
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        
        # Create Basic Auth token
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }
        
        # Initialize sentence transformer model
        print("Loading sentence transformer...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_all_categories(self):
        """Get all WordPress categories"""
        categories = []
        page = 1
        while True:
            print("Fetching categories page", page)
            r = requests.get(f"{self.base_url}/categories?per_page=100&page={page}", headers=self.headers)
            data = r.json()
            if not data:
                break
            categories.extend(data)
            page += 1
        return categories

    def get_uncategorized_posts(self):
        """Get posts that are either only in 'Uncategorized' or have no categories at all"""
        posts = []
        uncategorized_posts = []
        page = 1

        while True:
            r = requests.get(
                f"{self.base_url}/posts?per_page=100&page={page}",
                headers=self.headers
            )
            if r.status_code == 400:
                data = r.json()
                if data.get("code") == "rest_post_invalid_page_number":
                    break
                else:
                    r.raise_for_status()
            else:
                r.raise_for_status()

            try:
                data = r.json()
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Error decoding JSON on page {page}: {e}")

            if not data:
                break

            posts.extend(data)
            page += 1

        for post in posts:
            cat_ids = post.get("categories", [])
            if not cat_ids or cat_ids == [1]:  # either no categories or only uncategorized
                uncategorized_posts.append(post)

        if not uncategorized_posts:
            raise RuntimeError("No uncategorized or category-less posts found.")

        return uncategorized_posts


    def create_category(self, name):
        """Create a new category"""
        slug = make_slug(name)
        r = requests.post(f"{self.base_url}/categories", headers=self.headers, json={"name": name, "slug": slug})
        return r.json().get("id")

    def update_post_category(self, post_id, cat_id):
        """Update a post's category"""
        requests.put(f"{self.base_url}/posts/{post_id}", headers=self.headers, json={"categories": [cat_id]})
