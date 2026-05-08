import os
import json
import urllib.parse
import random
import time
from groq import Groq
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ==========================================
# 1. CONFIGURATION
# ==========================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BLOG_ID = "8729006952403006645"

client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 2. AI CONTENT ENGINE
# ==========================================
def get_diverse_ai_topic():
    styles = ["controversial AI future", "Gemini AI new updates", "Top 10 AI tools", "New AI videos generation", "AI coding secrets", "Yop AI hidden fir education", "AI income niches"]
    prompt = f"Generate ONE unique, viral blog title about AI technology. Style: {random.choice(styles)}. No quotes."
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0
    )
    return completion.choices[0].message.content.strip().replace('"', '')

def generate_article_body(title):
    prompt = f"Write a professional, 1,300+ word SEO blog post in HTML about '{title}'. Use <h2>, <h3>, <p>, <ul>. Tone: Professional."
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a senior tech writer."}, {"role": "user", "content": prompt}],
        max_tokens=5000
    )
    return completion.choices[0].message.content.replace("```html", "").replace("```", "").strip()

# Halkan waxaa lagu daray mashiin sawirka sharaxaya oo title-ka raacaya
def generate_image_prompt(title):
    prompt = f"Create two short images, 8k quality, descriptive image prompt for an AI generator based on this title: '{title}'. Focus on variety: can be ai and text or a computer, digital art, ai laptop, futuristic landscape, or abstract tech. Avoid only showing robot heads. Max 15 words."
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    return completion.choices[0].message.content.strip().replace('"', '')

def get_image_url(prompt):
    seed = random.randint(1, 1000000)
    # Waxaan ku daray ereyo tayo kordhinaya
    enhanced_prompt = f"{prompt}, high quality, cinematic lighting, 8k resolution"
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true&seed={seed}"

# ==========================================
# 3. BLOGGER UPLOADER
# ==========================================
def publish_to_blogger(title, content):
    try:
        token_data = json.loads(os.getenv("BLOGGER_TOKEN"))
        creds = Credentials.from_authorized_user_info(token_data)
        service = build('blogger', 'v3', credentials=creds)
        post_body = {"title": title, "content": content, "labels": ["AI", "Tech"]}
        service.posts().insert(blogId=BLOG_ID, body=post_body, isDraft=False).execute()
        print(f"✅ Published: {title}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_automation():
    for i in range(2): 
        title = get_diverse_ai_topic()
        
        # Halkan waxaan ku kicinaynaa sharaxaadda sawirka cusub
        img_desc = generate_image_prompt(title)
        header_img = get_image_url(img_desc)
        
        body_html = generate_article_body(title)
        header_tag = f'<div style="text-align:center;"><img src="{header_img}" referrerpolicy="no-referrer" style="width:100%; border-radius:12px;"></div><br>'
        
        publish_to_blogger(title, header_tag + body_html)
        time.sleep(5)

if __name__ == "__main__":
    run_automation()
