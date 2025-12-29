import requests
from bs4 import BeautifulSoup
import validators
from urllib.parse import urlparse

def analyze_url(url):
    if not validators.url(url):
        return {"error": "Invalid URL format"}

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Could not reach website: {str(e)}"}

    soup = BeautifulSoup(response.text, 'lxml')
    results = []
    score = 0
    total_checks = 8

    # 1. Title Tag
    title = soup.find('title')
    title_text = title.string if title else ""
    if title_text:
        length = len(title_text)
        if 50 <= length <= 60:
            results.append({"check": "Title Tag", "status": "passed", "msg": f"Perfect length ({length} chars)."})
            score += 1
        else:
            results.append({"check": "Title Tag", "status": "warning", "msg": f"Title is {length} chars. Aim for 50-60."})
    else:
        results.append({"check": "Title Tag", "status": "failed", "msg": "Missing title tag."})

    # 2. Meta Description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    desc_text = meta_desc['content'] if meta_desc else ""
    if desc_text:
        length = len(desc_text)
        if 120 <= length <= 160:
            results.append({"check": "Meta Description", "status": "passed", "msg": "Optimal length."})
            score += 1
        else:
            results.append({"check": "Meta Description", "status": "warning", "msg": f"Length is {length}. Aim for 120-160."})
    else:
        results.append({"check": "Meta Description", "status": "failed", "msg": "Missing meta description."})

    # 3. H1 Tag
    h1s = soup.find_all('h1')
    if len(h1s) == 1:
        results.append({"check": "H1 Header", "status": "passed", "msg": "Exactly one H1 found."})
        score += 1
    elif len(h1s) > 1:
        results.append({"check": "H1 Header", "status": "warning", "msg": "Multiple H1 tags found."})
    else:
        results.append({"check": "H1 Header", "status": "failed", "msg": "No H1 tag found."})

    # 4. H2 Tags
    h2s = soup.find_all('h2')
    if len(h2s) > 0:
        results.append({"check": "H2 Headers", "status": "passed", "msg": f"Found {len(h2s)} H2 tags."})
        score += 1
    else:
        results.append({"check": "H2 Headers", "status": "warning", "msg": "No H2 tags found for structure."})

    # 5. Image Alts
    images = soup.find_all('img')
    images_without_alt = [img for img in images if not img.get('alt')]
    if not images_without_alt:
        results.append({"check": "Image Alt Text", "status": "passed", "msg": "All images have alt tags."})
        score += 1
    else:
        results.append({"check": "Image Alt Text", "status": "warning", "msg": f"{len(images_without_alt)} images missing alt text."})

    # 6. Canonical Tag
    canonical = soup.find('link', rel='canonical')
    if canonical:
        results.append({"check": "Canonical Tag", "status": "passed", "msg": "Canonical URL is set."})
        score += 1
    else:
        results.append({"check": "Canonical Tag", "status": "failed", "msg": "Missing canonical tag."})

    # 7. Open Graph Tags
    og_title = soup.find('meta', property='og:title')
    if og_title:
        results.append({"check": "Social (OG) Tags", "status": "passed", "msg": "Open Graph tags present."})
        score += 1
    else:
        results.append({"check": "Social (OG) Tags", "status": "warning", "msg": "No Open Graph tags found."})

    # 8. URL Structure
    path = urlparse(url).path
    if len(path) > 1 and "_" not in path:
        results.append({"check": "URL Structure", "status": "passed", "msg": "Clean URL (no underscores)."})
        score += 1
    else:
        results.append({"check": "URL Structure", "status": "warning", "msg": "URL could be more SEO friendly."})

    final_score = int((score / total_checks) * 100)
    return {"score": final_score, "results": results, "url": url}