import feedparser
import datetime
import html
import re
from collections import defaultdict

# ===================== 配置区 =====================
RSS_URLS = [
    "https://news.google.com/rss/search?q=城乡规划+国土空间&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=城市更新+老旧小区&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=乡村振兴+美丽乡村&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=城市体检+安全韧性&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=智能建造+数智孪生&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
]

KEYWORDS = [
    "存量提质增效", "城市更新十五五规划", "人本更新", "城市体检",
    "安全韧性", "四好建设", "城乡融合", "新质生产力",
    "临时使用", "规划转型", "智能建造", "数智孪生"
]

# 显示别名（修复引号）
KEYWORD_ALIAS = {
    "存量提质增效": "存量提质增效",
    "城市更新十五五规划": "城市更新（十五五）规划",
    "人本更新": "人本更新",
    "城市体检": "城市体检",
    "安全韧性": "安全韧性",
    "四好建设": "四好建设",
    "城乡融合": "城乡融合",
    "新质生产力": "新质生产力",
    "临时使用": "临时使用",
    "规划转型": "规划转型",
    "智能建造": "智能建造",
    "数智孪生": "数智孪生"
}

SITE_TITLE = "城乡规划 · 热点新闻聚合"
# ===============================================

def extract_region(text):
    text = text.lower()
    if re.search(r'广州|越秀|天河|海珠|荔湾|白云|黄埔|番禺|花都|南沙|从化|增城', text):
        return "广州市"
    elif re.search(r'广东|深圳|东莞|佛山|珠海|中山|惠州|江门|肇庆|汕头|湛江', text):
        return "广东省"
    else:
        return "全国"

def match_keywords(text):
    """返回匹配的关键词列表，若无匹配则返回空列表（这条新闻将被丢弃）"""
    matched = []
    for kw in KEYWORDS:
        if kw == "城市更新十五五规划":
            if re.search(r'城市更新.*?十五五|十五五.*?城市更新', text):
                matched.append(kw)
        elif kw in text:
            matched.append(kw)
    return matched  # 不再返回 ["其他"]

def fetch_news():
    all_entries = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                full_text = title + " " + summary
                pub_time = entry.get('published', entry.get('updated', ''))
                if not pub_time:
                    continue
                region = extract_region(full_text)
                keywords = match_keywords(full_text)
                # 如果没有任何关键词匹配，则丢弃这条新闻（不收录）
                if not keywords:
                    continue
                entry_data = {
                    'title': title,
                    'link': entry.get('link', '#'),
                    'source': entry.get('source', {}).get('title', '未知来源'),
                    'published': pub_time,
                    'region': region,
                    'keywords': keywords
                }
                all_entries.append(entry_data)
        except Exception as e:
            print(f"抓取 {url} 时出错，但继续：{e}")
            continue
    return all_entries

def generate_html(entries):
    entries.sort(key=lambda x: x['published'], reverse=True)
    
    # 按关键词分组（每条新闻可能出现在多个关键词下）
    grouped_by_keyword = defaultdict(list)
    for item in entries:
        for kw in item['keywords']:
            grouped_by_keyword[kw].append(item)
    
    # 强制显示所有12个关键词，即使没有新闻，也显示卡片（0条）
    ordered_keywords = KEYWORDS  # 全部显示，保持顺序

    # 以下 CSS 和 HTML 结构与之前相同（略作优化）
    css = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f4f7fb;
            color: #1e2a3a;
            padding: 1.5rem 1.5rem;
            line-height: 1.5;
        }
        .container { max-width: 1440px; margin: 0 auto; }
        .banner {
            background: linear-gradient(135deg, #0b3b5c 0%, #1d7a8c 100%);
            border-radius: 16px;
            padding: 1.2rem 2rem;
            margin-bottom: 1.8rem;
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.8rem;
        }
        .banner .banner-left { display: flex; align-items: center; gap: 1rem; }
        .banner .banner-icon { font-size: 2.4rem; line-height: 1; background: rgba(255,255,255,0.15); padding: 0.2rem 0.6rem; border-radius: 40px; }
        .banner .banner-keyword { font-size: 1.6rem; font-weight: 700; }
        .banner .banner-tag { background: rgba(255,255,255,0.2); padding: 0.15rem 1rem; border-radius: 30px; font-size: 0.85rem; }
        @media (max-width: 600px) {
            .banner { padding: 1rem; flex-direction: column; align-items: flex-start; }
            .banner .banner-keyword { font-size: 1.2rem; }
        }
        .header { text-align: center; margin-bottom: 1.5rem; }
        .header h1 { font-size: 1.8rem; font-weight: 700; color: #0b3b5c; }
        .header p { font-size: 0.95rem; color: #4a5b6e; }
        .header .badge { display: inline-block; background: #1d7a8c; color: #fff; font-size: 0.75rem; padding: 0.1rem 0.8rem; border-radius: 20px; margin-top: 0.3rem; }
        .search-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            background: #fff;
            padding: 0.6rem 1.2rem;
            border-radius: 40px;
            border: 1px solid #dce5ef;
        }
        .search-bar input[type="text"] {
            flex: 1 1 180px;
            padding: 0.4rem 1rem;
            border: 1px solid #d0ddee;
            border-radius: 30px;
            font-size: 0.9rem;
            outline: none;
            min-width: 120px;
        }
        .search-bar input[type="text"]:focus { border-color: #1d7a8c; }
        .search-bar select {
            padding: 0.4rem 1rem;
            border: 1px solid #d0ddee;
            border-radius: 30px;
            font-size: 0.9rem;
            background: #fff;
            outline: none;
            min-width: 100px;
        }
        .search-bar .clear-btn {
            background: #e6eef9;
            border: none;
            padding: 0.3rem 1rem;
            border-radius: 30px;
            font-size: 0.8rem;
            cursor: pointer;
            color: #1d5a7a;
        }
        .search-bar .clear-btn:hover { background: #d0ddee; }
        @media (max-width: 600px) {
            .search-bar { border-radius: 16px; padding: 0.8rem; flex-direction: column; }
            .search-bar input[type="text"], .search-bar select { width: 100%; }
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.2rem;
        }
        .card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.2rem 1.2rem 1.2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
            border: 1px solid #e6ecf5;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .card .category {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid #ecf1f7;
            padding-bottom: 0.5rem;
            flex-shrink: 0;
        }
        .card .category .icon { font-size: 1.2rem; }
        .card .category h2 { font-size: 1.0rem; font-weight: 700; color: #0b3b5c; }
        .card .category .tag { margin-left: auto; background: #e6eef9; color: #1d5a7a; font-size: 0.6rem; font-weight: 600; padding: 0.05rem 0.6rem; border-radius: 20px; }
        .news-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            height: 300px;
            overflow-y: auto;
            padding-right: 4px;
            scrollbar-width: thin;
        }
        .news-list::-webkit-scrollbar { width: 3px; }
        .news-list::-webkit-scrollbar-track { background: #f0f4fa; border-radius: 3px; }
        .news-list::-webkit-scrollbar-thumb { background: #b0c4de; border-radius: 3px; }
        .news-list li {
            border-bottom: 1px dashed #e6ecf5;
            padding-bottom: 0.5rem;
            flex-shrink: 0;
        }
        .news-list li:last-child { border-bottom: none; padding-bottom: 0; }
        .news-list a {
            text-decoration: none;
            color: #1e2a3a;
            font-weight: 500;
            font-size: 0.88rem;
            display: block;
            transition: color 0.2s;
        }
        .news-list a:hover { color: #117a8b; }
        .news-list .meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.7rem;
            color: #7a8c9e;
            margin-top: 0.15rem;
            flex-wrap: wrap;
            gap: 0.2rem;
        }
        .news-list .meta .source { background: #f0f4fa; padding: 0.02rem 0.5rem; border-radius: 10px; color: #3d5a73; }
        .news-list .meta .date { color: #8a9bab; }
        .region-tag { display: inline-block; background: #d0e6f0; color: #0b4a5c; padding: 0 8px; border-radius: 12px; font-size: 0.6rem; margin-right: 2px; }
        .card-footer { margin-top: 0.5rem; padding-top: 0.4rem; border-top: 1px solid #ecf1f7; font-size: 0.65rem; color: #8a9bab; text-align: right; flex-shrink: 0; }
        .footer { margin-top: 2.5rem; text-align: center; font-size: 0.8rem; color: #6b7e93; border-top: 1px solid #dce5ef; padding-top: 1.2rem; }
        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 44px;
            height: 44px;
            background: #1d7a8c;
            color: #fff;
            border: none;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(29, 122, 140, 0.3);
            transition: opacity 0.3s ease, transform 0.3s ease;
            opacity: 0;
            visibility: hidden;
            transform: translateY(15px);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .back-to-top.visible { opacity: 1; visibility: visible; transform: translateY(0); }
        .back-to-top:hover { background: #0b5a6a; }
        @media (max-width: 600px) {
            .back-to-top { bottom: 20px; right: 20px; width: 38px; height: 38px; font-size: 16px; }
            .grid { grid-template-columns: 1fr; }
            .news-list { height: 220px; }
        }
    </style>
    """

    html_lines = []
    html_lines.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_lines.append(f'<title>{SITE_TITLE}</title>')
    html_lines.append(css)
    html_lines.append('</head><body>')
    html_lines.append('<div class="container">')

    html_lines.append(f'''
    <div class="banner">
        <div class="banner-left">
            <span class="banner-icon">🏙️</span>
            <span class="banner-keyword">{SITE_TITLE}</span>
        </div>
        <span class="banner-tag">📅 {datetime.datetime.now().strftime("%Y年%m月%d日")} · 共{len(entries)}条</span>
    </div>
    ''')

    html_lines.append('''
    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="🔍 搜索关键词或标题">
        <select id="regionFilter">
            <option value="">所有地域</option>
            <option value="全国">全国</option>
            <option value="广东省">广东省</option>
            <option value="广州市">广州市</option>
        </select>
        <button class="clear-btn" id="clearBtn">清除筛选</button>
    </div>
    ''')

    html_lines.append('<div class="grid" id="newsGrid">')
    for kw in ordered_keywords:
        items = grouped_by_keyword.get(kw, [])  # 如果没有新闻，则为空列表
        display_name = KEYWORD_ALIAS.get(kw, kw)
        icon = "📌"
        html_lines.append(f'<div class="card" data-keyword="{kw}">')
        html_lines.append(f'<div class="category"><span class="icon">{icon}</span><h2>{display_name}</h2><span class="tag">{len(items)}条</span></div>')
        html_lines.append('<ul class="news-list">')
        if items:
            for item in items[:50]:
                title = html.escape(item['title'])
                link = item['link']
                source = html.escape(item.get('source', '未知来源'))
                pub = item['published'][:10] if len(item['published']) > 10 else item['published']
                region_str = item['region']
                region_tag = f'<span class="region-tag">📍{region_str}</span>'
                html_lines.append(f'''
                <li data-title="{title}" data-region="{region_str}" data-keywords="{kw}">
                    <a href="{link}" target="_blank">{title}</a>
                    <div class="meta">
                        <span class="source">{source}</span>
                        <span>{region_tag} <span class="date">{pub}</span></span>
                    </div>
                </li>
                ''')
        else:
            # 如果该关键词下没有新闻，显示提示信息
            html_lines.append('<li style="color:#999; font-size:0.8rem; text-align:center; padding:1rem 0;">暂无相关新闻</li>')
        html_lines.append('</ul>')
        html_lines.append('<div class="card-footer">点击标题查看原文</div>')
        html_lines.append('</div>')
    html_lines.append('</div>')

    html_lines.append(f'''
    <div class="footer">
        🤖 机器人每周一自动更新 · 按关键词自动分类 · 数据来源于 RSS 聚合<br>
        <span style="font-size:0.7rem;">更新于 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
    </div>
    ''')

    html_lines.append('</div>')

    html_lines.append('''
    <button class="back-to-top" id="backToTop" aria-label="回到顶部">↑</button>
    <script>
        (function() {
            const searchInput = document.getElementById('searchInput');
            const regionFilter = document.getElementById('regionFilter');
            const clearBtn = document.getElementById('clearBtn');
            const allItems = document.querySelectorAll('.news-list li');
            const cards = document.querySelectorAll('.card');

            function filter() {
                const keyword = searchInput.value.trim().toLowerCase();
                const region = regionFilter.value;

                allItems.forEach(item => {
                    const title = (item.getAttribute('data-title') || '').toLowerCase();
                    const itemRegion = item.getAttribute('data-region') || '';
                    const matchKeyword = keyword === '' || title.includes(keyword);
                    const matchRegion = region === '' || itemRegion === region;
                    item.style.display = (matchKeyword && matchRegion) ? '' : 'none';
                });

                cards.forEach(card => {
                    const list = card.querySelector('.news-list');
                    const items = list.querySelectorAll('li');
                    let visibleCount = 0;
                    items.forEach(li => { if (li.style.display !== 'none') visibleCount++; });
                    const tag = card.querySelector('.category .tag');
                    if (tag) tag.textContent = visibleCount + '条';
                });
            }

            searchInput.addEventListener('input', filter);
            regionFilter.addEventListener('change', filter);
            clearBtn.addEventListener('click', function() {
                searchInput.value = '';
                regionFilter.value = '';
                filter();
            });

            var btn = document.getElementById('backToTop');
            window.addEventListener('scroll', function() {
                if (window.scrollY > 300) {
                    btn.classList.add('visible');
                } else {
                    btn.classList.remove('visible');
                }
            });
            btn.addEventListener('click', function() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        })();
    </script>
    </body></html>
    ''')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    print("网页生成成功！")

if __name__ == "__main__":
    print("奶奶稍等，机器人开始抓新闻了...")
    news = fetch_news()
    print(f"共抓取 {len(news)} 条新闻，正在排版...")
    generate_html(news)
    print("全部搞定！")
