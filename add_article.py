# -*- coding: utf-8 -*-
"""
ZooTecture 自動新增文章腳本 add_article.py
用法:
  python add_article.py --title "文章標題" --category "寵物空間規劃" --content-file article.txt --images img1.jpg img2.jpg
  python add_article.py --config new_article.json

功能:
  1. 自動產生 post-XXX.html (完整SEO/AIO結構)
  2. 自動更新 blog.html 文章列表
  3. 自動更新對應分類頁 col*.html
  4. 自動更新 articles_meta.json
  5. 自動更新 sitemap.xml
  6. 自動加入3-5篇相關文章的延伸閱讀連結
  7. 自動複製圖片到 images/ 目錄
"""

import os, sys, json, re, argparse, shutil
from pathlib import Path
from datetime import datetime

BASE = Path(r"D:\_zoot_webzone\alone\sites\petblog")
POSTS = BASE / "posts"
IMGS = BASE / "images"
META_FILE = BASE / "articles_meta.json"
SITEMAP_FILE = BASE / "sitemap.xml"
BLOG_FILE = BASE / "blog.html"

# Category to col page mapping
CAT_TO_COL = {
    "狗狗日記": "dog-diary.html",
    "貓咪物語": "cat-story.html",
    "寵物教育": "pet-education.html",
    "寵物健康": "pet-health.html",
    "居家設計": "home-design.html",
    "萌寵日常": "pet-daily.html",
    "異寵世界": "pet-daily.html",
    "寵物空間規劃": "pet-space.html",
    "戶外探險": "outdoor-adventure.html",
    "節日寵物": "outdoor-adventure.html",
    "寵物藝術": "pet-art.html",
}

VALID_CATEGORIES = list(CAT_TO_COL.keys())


def load_meta():
    """Load existing articles metadata"""
    if META_FILE.exists():
        with open(META_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_meta(articles):
    """Save articles metadata"""
    with open(META_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


def get_next_id(articles):
    """Get the next article ID"""
    if not articles:
        return 1
    return max(a['id'] for a in articles) + 1


def find_related_articles(articles, category, exclude_id, limit=5):
    """Find related articles in the same category"""
    related = [a for a in articles if a.get('category') == category and a['id'] != exclude_id]
    # If not enough in same category, get from all
    if len(related) < limit:
        others = [a for a in articles if a.get('category') != category and a['id'] != exclude_id]
        related.extend(others[:limit - len(related)])
    return related[:limit]


def generate_post_html(article, related_articles):
    """Generate full post HTML with SEO/AIO structure"""
    aid = article['id']
    title = article['title']
    category = article['category']
    meta_desc = article['meta_desc']
    keywords = article['keywords']
    images = article['images']
    content = article.get('content', '')
    excerpt = article.get('excerpt', meta_desc[:100])

    # Generate image gallery HTML
    img_gallery = ""
    for i, img in enumerate(images):
        img_name = img.replace(" ", "_")
        alt_text = f"{title} - 圖片{i+1}"
        img_gallery += f'''<div class="article-image">
<img src="../images/{img_name}" alt="{alt_text}" loading="lazy">
<p class="img-caption">{alt_text}</p>
</div>'''

    # Generate related articles links
    related_html = ""
    for ra in related_articles:
        raid = ra['id']
        rtitle = ra['title']
        related_html += f'<li><a href="post-{raid:03d}.html">{rtitle}</a></li>'

    # Generate FAQ schema (4 Q&A)
    faqs = article.get('faqs', [
        {"q": f"{title}最重要的是什麼？", "a": f"核心重點是{excerpt}"},
        {"q": "適合什麼樣的飼主？", "a": "適合所有想要提升寵物生活品質的飼主，不論新手或資深飼主都能受益。"},
        {"q": "需要預算多少？", "a": "根據實際需求調整，從DIY到專業規劃都有對應方案。"},
        {"q": "多久可以看到效果？", "a": "通常實施後1-2週即可觀察到寵物行為與生活品質的改善。"},
    ])
    faq_schema = ""
    for faq in faqs:
        faq_schema += f'''{{
          "@type": "Question",
          "name": "{faq['q']}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{faq['a']}"
          }}
        }},'''
    faq_schema = faq_schema.rstrip(',')

    # AIO answer box
    aio_answer = article.get('aio_answer', f"**{title}**的核心要點：{excerpt}。建議從評估現有空間與寵物需求開始，逐步實施。")

    # Bold key terms in content
    content_html = content
    for term in [title, category, "寵物", "空間", "設計", "訓練", "健康", "營養"]:
        if term and len(term) > 1:
            content_html = content_html.replace(term, f"<strong>{term}</strong>", 1)

    html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{', '.join(keywords)}">
<meta name="robots" content="index, follow, max-snippet:-1">
<link rel="canonical" href="https://zootecture.com/posts/post-{aid:03d}.html">
<meta property="og:title" content="{title} | ZooTecture 入梯毛孩">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:image" content="../images/{images[0].replace(' ', '_') if images else 'logo.jpg'}">
<title>{title} | ZooTecture 入梯毛孩</title>
<link rel="icon" type="image/png" href="../images/favicon.png">
<link rel="stylesheet" href="../css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{faq_schema}]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "image": "../images/{images[0].replace(' ', '_') if images else 'logo.jpg'}",
  "author": {{"@type": "Organization", "name": "ZooTecture 入梯毛孩"}},
  "publisher": {{"@type": "Organization", "name": "ZooTecture"}},
  "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
  "dateModified": "{datetime.now().strftime('%Y-%m-%d')}"
}}
</script>
</head>
<body>
<nav class="site-nav">
<div class="nav-container">
<a href="../index.html" class="nav-logo">🐾 ZooTecture 入梯毛孩</a>
<div class="nav-links">
<a href="../index.html">🏠 首頁</a>
<a href="../blog.html">📚 文章總覽</a>
<a href="../{CAT_TO_COL.get(category, 'blog.html')}">📂 {category}</a>
</div>
</div>
</nav>

<main class="article-main">
<article class="article-content">
<div class="aio-box">
<h3>💡 快速回答</h3>
<p>{aio_answer}</p>
</div>

<h1>{title}</h1>
<div class="article-meta">
<span class="meta-cat">{category}</span>
<span class="meta-date">{datetime.now().strftime('%Y年%m月%d日')}</span>
</div>

<div class="article-body">
{content_html}
</div>

{img_gallery}

<section class="faq-section">
<h2>❓ 常見問題 FAQ</h2>
{"".join(f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>' for f in faqs)}
</section>

<section class="key-points">
<h2>📌 重點整理</h2>
<ul>
<li>了解<strong>{category}</strong>的核心需求與原則</li>
<li>根據實際環境與預算制定可行方案</li>
<li>逐步實施並觀察寵物反應調整</li>
<li>定期維護與優化，確保長期效果</li>
</ul>
</section>

<section class="related-articles">
<h2>🔗 延伸閱讀</h2>
<ul>
{related_html}
</ul>
</section>

<div class="article-nav">
<a href="post-{aid-1:03d}.html" class="nav-prev">← 上一篇</a>
<a href="../blog.html" class="nav-list">文章列表</a>
<a href="post-{aid+1:03d}.html" class="nav-next">下一篇 →</a>
</div>
</article>
</main>

<footer class="site-footer">
<p>&copy; {datetime.now().year} ZooTecture 入梯毛孩 | 共 250+ 篇寵物知識文章</p>
<p><a href="../index.html">首頁</a> | <a href="../blog.html">文章總覽</a> | <a href="../sitemap.xml">Sitemap</a></p>
</footer>

<button class="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<script>
window.addEventListener('scroll',function(){{var b=document.querySelector('.back-top');if(window.scrollY>300)b.classList.add('show');else b.classList.remove('show');}});
</script>
</body>
</html>'''
    return html


def update_blog_html(article):
    """Insert new article card into blog.html"""
    if not BLOG_FILE.exists():
        print(f"  Warning: {BLOG_FILE} not found, skipping blog update")
        return

    with open(BLOG_FILE, 'r', encoding='utf-8') as f:
        c = f.read()

    aid = article['id']
    title = article['title']
    category = article['category']
    excerpt = article.get('excerpt', article['meta_desc'][:80])
    img = article['images'][0].replace(" ", "_") if article['images'] else "logo.jpg"

    new_card = f'''<div class="article-card" data-cat="{category}" onclick="location.href='posts/post-{aid:03d}.html'">
<img src="images/{img}" alt="{title}" loading="lazy">
<div class="card-body">
<span class="card-cat">{category}</span>
<h3>{title}</h3>
<p>{excerpt}...</p>
</div>
</div>'''

    # Insert after the first article-card in the grid
    if 'class="article-grid"' in c:
        # Find the article-grid div and insert after its opening tag
        pattern = r'(<div class="article-grid">)'
        c = re.sub(pattern, r'\1\n' + new_card, c, count=1)
    elif 'class="posts-grid"' in c:
        pattern = r'(<div class="posts-grid">)'
        c = re.sub(pattern, r'\1\n' + new_card, c, count=1)
    else:
        print(f"  Warning: article-grid not found in blog.html")
        return

    # Update article count
    c = re.sub(r'(\d+)\s*篇文章', lambda m: str(int(m.group(1)) + 1) + ' 篇文章', c, count=1)

    with open(BLOG_FILE, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  Updated blog.html with new article card")


def update_category_page(article):
    """Add new article to the corresponding category page"""
    col_file = CAT_TO_COL.get(article['category'])
    if not col_file:
        print(f"  Warning: no category page for {article['category']}")
        return

    col_path = BASE / col_file
    if not col_path.exists():
        print(f"  Warning: {col_path} not found")
        return

    with open(col_path, 'r', encoding='utf-8') as f:
        c = f.read()

    aid = article['id']
    title = article['title']
    category = article['category']
    excerpt = article.get('excerpt', article['meta_desc'][:80])
    img = article['images'][0].replace(" ", "_") if article['images'] else "logo.jpg"

    new_card = f'''<div class="article-card" onclick="location.href='posts/post-{aid:03d}.html'">
<img src="images/{img}" alt="{title}" loading="lazy">
<div class="card-body">
<span class="card-cat">{category}</span>
<h4>{title}</h4>
<p>{excerpt}...</p>
</div></div>'''

    # Insert into article-grid
    if 'class="article-grid"' in c:
        pattern = r'(<div class="article-grid">)'
        c = re.sub(pattern, r'\1\n' + new_card, c, count=1)

    with open(col_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  Updated {col_file} with new article")


def update_sitemap(article):
    """Add new URL to sitemap.xml"""
    if not SITEMAP_FILE.exists():
        # Create basic sitemap
        sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://zootecture.com/</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
<url><loc>https://zootecture.com/blog.html</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
</urlset>'''
        with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
            f.write(sitemap)

    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        c = f.read()

    aid = article['id']
    new_url = f'<url><loc>https://zootecture.com/posts/post-{aid:03d}.html</loc><lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'

    if f'post-{aid:03d}.html' not in c:
        c = c.replace('</urlset>', new_url + '\n</urlset>')
        with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"  Updated sitemap.xml")


def copy_images(image_paths):
    """Copy images to images/ directory, convert to WebP, return filenames"""
    from PIL import Image
    copied = []
    for img_path in image_paths:
        p = Path(img_path)
        if p.exists():
            ext = p.suffix.lower()
            if ext in ['.jpg', '.jpeg', '.png'] and 'favicon' not in p.name:
                # Convert to WebP
                webp_name = p.stem + '.webp'
                dst = IMGS / webp_name
                if not dst.exists():
                    img = Image.open(p)
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    img.save(dst, 'WEBP', quality=82, method=6)
                    print(f"  Converted: {p.name} -> {webp_name}")
                copied.append(webp_name)
            else:
                dst = IMGS / p.name
                if not dst.exists():
                    shutil.copy2(p, dst)
                    print(f"  Copied image: {p.name}")
                copied.append(p.name)
        else:
            webp_name = Path(img_path).stem + '.webp'
            copied.append(webp_name)
    return copied


def add_article(title, category, content, images, meta_desc=None, keywords=None, excerpt=None, faqs=None, aio_answer=None):
    """Main function to add a new article"""
    print(f"\n{'='*60}")
    print(f"新增文章: {title}")
    print(f"分類: {category}")
    print(f"{'='*60}")

    # Validate category
    if category not in VALID_CATEGORIES:
        print(f"Error: 無效分類 '{category}'")
        print(f"有效分類: {', '.join(VALID_CATEGORIES)}")
        return None

    # Load existing articles
    articles = load_meta()
    new_id = get_next_id(articles)
    print(f"  新文章ID: {new_id}")

    # Default values
    if not meta_desc:
        meta_desc = f"{title} - {category}完整指南，ZooTecture 入梯毛孩提供專業寵物知識。"
    if not keywords:
        keywords = [title, category, "寵物", "ZooTecture", "入梯毛孩", "寵物知識"]
    if not excerpt:
        excerpt = meta_desc[:100]

    # Copy images
    image_names = copy_images(images)

    # Create article metadata
    article = {
        "id": new_id,
        "title": title,
        "category": category,
        "meta_desc": meta_desc,
        "keywords": keywords,
        "images": image_names,
        "excerpt": excerpt,
        "content": content,
        "faqs": faqs,
        "aio_answer": aio_answer,
    }

    # Find related articles
    related = find_related_articles(articles, category, new_id)
    print(f"  找到 {len(related)} 篇相關文章")

    # Generate post HTML
    post_html = generate_post_html(article, related)
    post_file = POSTS / f"post-{new_id:03d}.html"
    with open(post_file, 'w', encoding='utf-8') as f:
        f.write(post_html)
    print(f"  產生文章頁: {post_file.name}")

    # Add to metadata (remove content to keep file small)
    article_meta = {k: v for k, v in article.items() if k != 'content'}
    articles.append(article_meta)
    save_meta(articles)
    print(f"  更新 articles_meta.json (共 {len(articles)} 篇)")

    # Update blog.html
    update_blog_html(article)

    # Update category page
    update_category_page(article)

    # Update sitemap
    update_sitemap(article)

    print(f"\n✅ 文章新增完成!")
    print(f"   文章頁: posts/post-{new_id:03d}.html")
    print(f"   文章總覽: blog.html")
    print(f"   分類頁: {CAT_TO_COL.get(category)}")
    print(f"   Sitemap: sitemap.xml")
    return new_id


def main():
    parser = argparse.ArgumentParser(description='ZooTecture 自動新增文章腳本')
    parser.add_argument('--title', type=str, help='文章標題')
    parser.add_argument('--category', type=str, help=f'分類: {", ".join(VALID_CATEGORIES)}')
    parser.add_argument('--content', type=str, help='文章內容(HTML)')
    parser.add_argument('--content-file', type=str, help='文章內容檔案路徑')
    parser.add_argument('--images', nargs='+', help='圖片路徑(可多張)')
    parser.add_argument('--meta-desc', type=str, help='Meta description')
    parser.add_argument('--keywords', nargs='+', help='SEO關鍵字')
    parser.add_argument('--excerpt', type=str, help='文章摘要')
    parser.add_argument('--config', type=str, help='JSON設定檔路徑')

    args = parser.parse_args()

    # Load from config file if specified
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        title = config.get('title')
        category = config.get('category')
        content = config.get('content', '')
        images = config.get('images', [])
        meta_desc = config.get('meta_desc')
        keywords = config.get('keywords')
        excerpt = config.get('excerpt')
        faqs = config.get('faqs')
        aio_answer = config.get('aio_answer')
    else:
        title = args.title
        category = args.category
        if args.content_file:
            with open(args.content_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = args.content or ""
        images = args.images or []
        meta_desc = args.meta_desc
        keywords = args.keywords
        excerpt = args.excerpt
        faqs = None
        aio_answer = None

    if not title or not category:
        print("錯誤: 請提供 --title 和 --category (或使用 --config)")
        print(f"有效分類: {', '.join(VALID_CATEGORIES)}")
        print("\n範例:")
        print('  python add_article.py --title "小公寓貓咪空間規劃" --category "寵物空間規劃" --content-file article.txt --images cat1.jpg cat2.jpg')
        print('  python add_article.py --config new_article.json')
        sys.exit(1)

    add_article(title, category, content, images, meta_desc, keywords, excerpt, faqs, aio_answer)


if __name__ == '__main__':
    main()
