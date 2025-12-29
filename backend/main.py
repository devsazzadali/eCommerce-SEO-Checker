import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# পাইথনকে আপনার প্রোজেক্ট ডিরেক্টরি চিনিয়ে দেওয়ার জন্য (Error: ModuleNotFoundError সমাধান করবে)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# utils ফোল্ডার থেকে আপনার এনালাইজার ইম্পোর্ট করা
try:
    from utils.seo_analyzer import analyze_url
except ImportError:
    # যদি utils ফোল্ডারটি সরাসরি না পাওয়া যায়
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    from utils.seo_analyzer import analyze_url

app = FastAPI()

# CORS সেটিংস: এটি আপনার Vercel ফ্রন্টএন্ডকে ডাটা পাঠানোর অনুমতি দিবে
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # প্রোডাকশনে আপনি আপনার Vercel URL দিতে পারেন
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

# রুট ইউআরএল চেক করার জন্য (ব্রাউজারে লিঙ্ক ওপেন করলে এটি দেখাবে)
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "E-commerce SEO Checker API is running smoothly!",
        "docs": "/docs"
    }

# মেইন এনালাইজ পোস্ট মেথড
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    try:
        data = analyze_url(request.url)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        # কোনো অপ্রত্যাশিত এরর হলে সেটি সার্ভার লগে দেখাবে
        print(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during analysis")

# Render পোর্টের জন্য রান কনফিগারেশন
if __name__ == "__main__":
    import uvicorn
    # Render অটোমেটিক $PORT ভেরিয়েবল দিয়ে থাকে, সেটি না পেলে ৮০০০ ব্যবহার করবে
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)