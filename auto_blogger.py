import os
import requests
import urllib.parse
import time
import random
from datetime import datetime
from groq import Groq
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ==========================================
# 1. CONFIGURATION
# ==========================================
GROQ_API_KEY = "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"
BLOG_ID = "8729006952403006645" 
TARGET_TIME = "20:38" # Saacadda East Africa (EAT)

client = Groq(api_key=GROQ_API_KEY)
SCOPES = ['https://www.googleapis.com/auth/blogger']

# ==========================================
# 2. AI CONTENT ENGINE
# ==========================================
def get_diverse_ai_topic():
    styles = [
        "a controversial opinion about AI's future",
        "a 'Top 10' list of hidden AI tools",
        "a deep technical secret about AI coding",
        "a warning about AI technologies that will fail",
        "a creative guide on making money with a specific AI niche"
    ]
    selected_style = random.choice(styles)
    print(f"🧠 Generating title using style: {selected_style}")
    
    prompt = f"Generate ONE unique, viral blog title about AI technology. Style: {selected_style}. Make it different from common titles. No quotes."
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0 # High randomness
    )
    return completion.choices[0].message.content.strip().replace('"', '')

def generate_article_body(title):
    print(f"✍️ Writing 1,300+ words for: {title}...")
    prompt = f"Write a professional, 1,300+ word SEO blog post in HTML about '{title}'. Use <h2>, <h3>, <p>, <ul>. Make it long and informative. No markdown blocks."
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a senior tech writer."}, {"role": "user", "content": prompt}],
        max_tokens=5000
    )
    return completion.choices[0].message.content.replace("```html", "").replace("```", "").strip()

def get_image_url(prompt):
    # Seed random ah si sawirku u noqdo mid cusub mar walba
    seed = random.randint(1, 1000000)
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true&seed={seed}"

# ==========================================
# 3. BLOGGER UPLOADER
# ==========================================
def authenticate_blogger():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('blogger', 'v3', credentials=creds)

def publish_to_blogger(title, content):
    try:
        service = authenticate_blogger()
        post_body = {"title": title, "content": content, "labels": ["AI", "Tech"]}
        request = service.posts().insert(blogId=BLOG_ID, body=post_body, isDraft=False)
        response = request.execute()
        print(f"✅ Published: {response.get('url')}")
    except Exception as e:
        print(f"❌ Blogger Error: {e}")

# ==========================================
# 4. CORE EXECUTION
# ==========================================
def run_automation():
    print(f"\n🚀 Starting Daily Post Cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for i in range(2): # 2 Post maalin walba
        print(f"\n--- Creating Post #{i+1} ---")
        title = get_diverse_ai_topic()
        header_img = get_image_url(f"hyper-realistic futuristic AI concept for {title}")
        body_html = generate_article_body(title)
        
        # New Image Formatting (Safer for Blogger)
        header_tag = f"""
        <div style="text-align:center;">
            <img src="{header_img}" referrerpolicy="no-referrer" style="width:100%; border-radius:12px; border: 1px solid #ddd;">
        </div><br>
        """
        final_content = header_tag + body_html
        publish_to_blogger(title, final_content)
        time.sleep(10) # Sugitaanka post-ka labaad

if __name__ == "__main__":
    print(f"🤖 Auto-Blogger is Active. Waiting for {TARGET_TIME} EAT...")
    
    while True:
        now = datetime.now().strftime("%H:%M")
        
        if now == TARGET_TIME:
            run_automation()
            print("\n✅ Done for today. Sleeping for 23 hours...")
            time.sleep(80000) # Sug ilaa maalinta xigta
            
        time.sleep(30) # Hubi saacadda 30-kii ilbidhiqsi kasta