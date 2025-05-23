import requests
import base64
import json
import re
from sentence_transformers import SentenceTransformer, util

# ----------- تنظیمات وردپرس -----------
USERNAME = "asimir"
PASSWORD = "ZSbd jn8P MewQ Rihf LYjQ L0Jp"
BASE_URL = "https://cms111.s4-tastewp.com/wp-json/wp/v2"

# ساخت توکن برای Basic Auth
token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
headers_wp = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# ----------- تنظیمات مدل -----------
print("Loading setence transformer ...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------- گرفتن همه کتگوری‌ها -----------
def get_all_categories():
    categories = []
    page = 1
    while True:
        print("while categories")
        r = requests.get(f"{BASE_URL}/categories?per_page=100&page={page}", headers=headers_wp)
        data = r.json()
        if not data:
            break
        categories.extend(data)
        page += 1
    return categories

# ----------- گرفتن همه پست‌های Uncategorzied -----------
def get_uncategorized_posts():
    posts = []
    page = 1
    while True:
        r = requests.get(f"{BASE_URL}/posts?categories=1&per_page=100&page={page}", headers=headers_wp)
        if r.status_code == 400:
            # چک کردن خطای صفحه خالی
            data = r.json()
            if data.get("code") == "rest_post_invalid_page_number":
                break
            else:
                r.raise_for_status()  # خطاهای دیگر رو پرت کن
        else:
            r.raise_for_status()  # اگر کد وضعیت غیر 200 بود خطا پرت کن

        try:
            data = r.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error decoding JSON on page {page}: {e}")

        if not data:
            # اگر لیست خالی بود یعنی پستی نیست
            break

        posts.extend(data)
        page += 1

    if not posts:
        raise RuntimeError("No uncategorized posts found.")

    return posts


# ----------- پیدا کردن نزدیک‌ترین کتگوری -----------
def find_best_category(candidate: str, categories):
    candidate_embedding = model.encode(candidate, convert_to_tensor=True)
    names = [cat['name'] for cat in categories]
    embeddings = model.encode(names, convert_to_tensor=True)
    similarities = util.cos_sim(candidate_embedding, embeddings)[0]
    best_idx = similarities.argmax().item()
    best_score = similarities[best_idx].item()
    if best_score >= 0.7:  # آستانه شباهت
        return categories[best_idx]['id'], categories[best_idx]['name']
    return None, None

def make_slug(name):
    # تبدیل به حروف کوچک
    slug = name.lower()
    # جایگزینی فاصله‌ها و زیرخط با خط تیره
    slug = re.sub(r'[\s_]+', '-', slug)
    # حذف کاراکترهای غیرحروف، غیرعدد و غیر خط تیره
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # حذف خط تیره‌های اضافی پشت سر هم
    slug = re.sub(r'-+', '-', slug)
    # حذف خط تیره ابتدای و انتهای رشته
    slug = slug.strip('-')
    return slug

# ----------- ساخت کتگوری جدید -----------
def create_category(name):
    slug = make_slug(name)
    r = requests.post(f"{BASE_URL}/categories", headers=headers_wp, json={"name": name, "slug": slug})
    return r.json().get("id")

# ----------- آپدیت پست با کتگوری جدید -----------
def update_post_category(post_id, cat_id):
    requests.put(f"{BASE_URL}/posts/{post_id}", headers=headers_wp, json={"categories": [cat_id]})

# ----------- استفاده از مدل Ollama (مبتنی بر لوکال) -----------
def get_category_from_ollama(text):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",  # or another model you have installed
        "prompt": f"Suggest an appropriate English category name for the following blog post content:\n\n{text}\n\nOnly return the category name, nothing else."
    })
    for line in r.iter_lines():
        print(line)
        if line:
            data = json.loads(line)
            if 'response' in data:
                return data['response'].strip()
    return "Uncategorized"

# ----------- اجرای اصلی -----------
def main():
    try:
        all_cats = get_all_categories()
        uncategorized_posts = get_uncategorized_posts()
        print("posts got")
        for post in uncategorized_posts:
            post_id = post['id']
            content = post['content']['rendered']
            suggested = get_category_from_ollama(content)

            matched_id, matched_name = find_best_category(suggested, all_cats)

            if matched_id:
                print(f"Matched category: {matched_name}")
                # update_post_category(post_id, matched_id)
            else:
                print(f"Creating new category: {suggested}")
                # new_cat_id = create_category(suggested)
                # update_post_category(post_id, new_cat_id)
    except Exception as e:
        print(f"Error: {e}")        

print("Starting script...")

if __name__ == "__main__":
    print("Starting main...")
    main()

    