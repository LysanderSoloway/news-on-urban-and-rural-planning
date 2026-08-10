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
    matched = []
    for kw in KEYWORDS:
        if kw == "城市更新十五五规划":
            if re.search(r'城市更新.*?十五五|十五五.*?城市更新', text):
                matched.append(kw)
        elif kw in text:
            matched.append(kw)
    return matched if matched else ["其他"]

def fetch_news():
    all_entries = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                full_text = title + " " + summary
                summary_clean = re.sub(r'<[^>]+>', '', summary)
                summary_clean = summary_clean[:180] + "..." if len(summary_clean) > 180 else summary_clean
                pub_time = entry.get('published', entry.get('updated', ''))
                if not pub_time:
                    continue
                region = extract_region(full_text)
                keywords = match_keywords(full_text)
                entry_data = {
                    'title': title,
                    'link': entry.get('link', '#'),
                    'summary': summary_clean,
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
    # 保留全部用于搜索过滤
    # 按地域分组（仍用于卡片分组）
    grouped = defaultdict(list)
    for item in entries[:150]:
        grouped[item['region']].append(item)

    # ========== 样式（与之前一致，增加搜索框样式）==========
    css = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f4f7fb;
            color: #1e2a3a;
            padding: 2rem 1.5rem;
            line-height: 1.6;
        }
        .container { max-width: 1440px; margin: 0 auto; }
        .banner {
            background: linear-gradient(135deg, #0b3b5c 0%, #1d7a8c 100%);
            border-radius: 24px;
            padding: 2rem 2.5rem;
            margin-bottom: 2.5rem;
            color: #fff;
            box-shadow: 0 10px 30px rgba(13, 67, 89, 0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .banner .banner-left {
            display: flex;
            align-items: center;
            gap: 1.2rem;
            flex: 1 1 auto;
        }
        .banner .banner-icon { font-size: 3.2rem; line-height: 1; background: rgba(255,255,255,0.15); padding: 0.3rem 0.8rem; border-radius: 60px; backdrop-filter: blur(4px); flex-shrink: 0; }
        .banner .banner-text { display: flex; flex-direction: column; }
        .banner .banner-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.7; font-weight: 600; }
        .banner .banner-keyword { font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-top: 0.1rem; text-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        .banner .banner-tag { background: rgba(255,255,255,0.2); backdrop-filter: blur(4px); padding: 0.2rem 1.2rem; border-radius: 40px; font-size: 0.9rem; font-weight: 500; white-space: nowrap; border: 1px solid rgba(255,255,255,0.15); }
        .banner .banner-indicators { display: flex; gap: 0.5rem; align-items: center; flex-shrink: 0; }
        .banner .dot { width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.3); transition: all 0.3s ease; cursor: pointer; }
        .banner .dot.active { background: #ffffff; transform: scale(1.3); box-shadow: 0 0 12px rgba(255,255,255,0.5); }
        @media (max-width: 700px) {
            .banner { flex-direction: column; align-items: flex-start; padding: 1.5rem; }
            .banner .banner-left { width: 100%; }
            .banner .banner-keyword { font-size: 1.8rem; }
            .banner .banner-indicators { align-self: center; margin-top: 0.2rem; }
        }
        .header { text-align: center; margin-bottom: 2rem; }
        .header h1 { font-size: 2.6rem; font-weight: 700; letter-spacing: 1px; background: linear-gradient(135deg, #0b3b5c, #1d7a8c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .header p { font-size: 1.1rem; color: #4a5b6e; margin-top: 0.5rem; border-bottom: 2px solid #d0ddee; padding-bottom: 1rem; max-width: 700px; margin-left: auto; margin-right: auto; }
        .header .badge { display: inline-block; background: #1d7a8c; color: #fff; font-size: 0.85rem; font-weight: 600; padding: 0.2rem 1rem; border-radius: 20px; margin-top: 0.5rem; }

        /* 搜索栏 */
        .search-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            background: #fff;
            padding: 1rem 1.5rem;
            border-radius: 60px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
            border: 1px solid #dce5ef;
        }
        .search-bar input[type="text"] {
            flex: 1 1 200px;
            padding: 0.6rem 1.2rem;
            border: 1px solid #d0ddee;
            border-radius: 40px;
            font-size: 1rem;
            outline: none;
            transition: border 0.2s;
            min-width: 150px;
        }
        .search-bar input[type="text"]:focus {
            border-color: #1d7a8c;
        }
        .search-bar select {
            padding: 0.6rem 1.2rem;
            border: 1px solid #d0ddee;
            border-radius: 40px;
            font-size: 1rem;
            background: #fff;
            outline: none;
            cursor: pointer;
            min-width: 120px;
        }
        .search-bar .clear-btn {
            background: #e6eef9;
            border: none;
            padding: 0.5rem 1.2rem;
            border-radius: 40px;
            font-size: 0.9rem;
            cursor: pointer;
            color: #1d5a7a;
            font-weight: 500;
            transition: background 0.2s;
        }
        .search-bar .clear-btn:hover {
            background: #d0ddee;
        }
        @media (max-width: 600px) {
            .search-bar {
                border-radius: 20px;
                padding: 1rem;
            }
            .search-bar input[type="text"], .search-bar select {
                width: 100%;
            }
        }

        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.8rem; }
        .card {
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(0, 20, 40, 0.06);
            padding: 1.6rem 1.8rem 1.8rem;
            transition: transform 0.25s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(209, 222, 240, 0.35);
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 16px 40px rgba(0, 30, 60, 0.10); border-color: #b2cbe0; }
        .card .category {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1.2rem;
            border-bottom: 2px solid #ecf1f7;
            padding-bottom: 0.7rem;
            flex-shrink: 0;
        }
        .card .category .icon { font-size: 1.6rem; line-height: 1; }
        .card .category h2 { font-size: 1.25rem; font-weight: 700; color: #0b3b5c; letter-spacing: 0.3px; }
        .card .category .tag { margin-left: auto; background: #e6eef9; color: #1d5a7a; font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.7rem; border-radius: 30px; white-space: nowrap; }
        .news-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
            height: 300px;
            overflow-y: auto;
            padding-right: 4px;
            scrollbar-width: thin;
        }
        .news-list::-webkit-scrollbar { width: 4px; }
        .news-list::-webkit-scrollbar-track { background: #f0f4fa; border-radius: 4px; }
        .news-list::-webkit-scrollbar-thumb { background: #b0c4de; border-radius: 4px; }
        .news-list li { border-bottom: 1px dashed #e6ecf5; padding-bottom: 0.7rem; flex-shrink: 0; }
        .news-list li:last-child { border-bottom: none; padding-bottom: 0; }
        .news-list a { text-decoration: none; color: #1e2a3a; font-weight: 500; font-size: 0.95rem; display: block; transition: color 0.2s; }
        .news-list a:hover { color: #117a8b; }
        .news-list .meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #7a8c9e; margin-top: 0.2rem; flex-wrap: wrap; gap: 0.3rem; }
        .news-list .meta .source { background: #f0f4fa; padding: 0.05rem 0.6rem; border-radius: 12px; color: #3d5a73; }
        .news-list .meta .date { color: #8a9bab; }
        .news-list .summary { font-size: 0.85rem; color: #4a5b6e; margin-top: 0.2rem; line-height: 1.4; }
        .keyword-tag { display: inline-block; background: #e6f0fa; color: #1a3c5e; padding: 0 10px; border-radius: 20px; font-size: 0.7rem; margin-right: 4px; }
        .region-tag { display: inline-block; background: #d0e6f0; color: #0b4a5c; padding: 0 10px; border-radius: 20px; font-size: 0.7rem; margin-right: 4px; }
        .card-footer { margin-top: 0.8rem; padding-top: 0.6rem; border-top: 1px solid #ecf1f7; font-size: 0.75rem; color: #8a9bab; text-align: right; flex-shrink: 0; }
        .footer { margin-top: 3.5rem; text-align: center; font-size: 0.9rem; color: #6b7e93; border-top: 1px solid #dce5ef; padding-top: 1.8rem; }
        .footer a { color: #1d7a8c; text-decoration: none; }
        .back-to-top {
            position: fixed;
            bottom: 40px;
            right: 40px;
            width: 52px;
            height: 52px;
            background: #1d7a8c;
            color: #fff;
            border: none;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(29, 122, 140, 0.35);
            transition: opacity 0.3s ease, transform 0.3s ease, background 0.2s ease;
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .back-to-top.visible { opacity: 1; visibility: visible; transform: translateY(0); }
        .back-to-top:hover { background: #0b5a6a; transform: translateY(-3px); box-shadow: 0 6px 20px rgba(29, 122, 140, 0.45); }
        .back-to-top:active { transform: scale(0.92); }
        @media (max-width: 600px) {
            .back-to-top { bottom: 24px; right: 24px; width: 46px; height: 46px; font-size: 20px; }
        }
        @media (max-width: 700px) {
            body { padding: 1rem; }
            .header h1 { font-size: 1.8rem; }
            .grid { grid-template-columns: 1fr; gap: 1.2rem; }
            .card { padding: 1.2rem; }
            .news-list { height: 260px; }
        }
    </style>
    """

    # ========== 构建 HTML ==========
    html_lines = []
    html_lines.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_lines.append(f'<title>{SITE_TITLE}</title>')
    html_lines.append(css)
    html_lines.append('</head><body>')
    html_lines.append('<div class="container">')

    # 横幅
    html_lines.append(f'''
    <div class="banner">
        <div class="banner-left">
            <div class="banner-icon">🏙️</div>
            <div class="banner-text">
                <div class="banner-label">城乡规划 · 新闻聚合</div>
                <div class="banner-keyword">{SITE_TITLE}</div>
            </div>
        </div>
        <div class="banner-tag">📅 {datetime.datetime.now().strftime("%Y年%m月%d日")}</div>
        <div class="banner-indicators"><span class="dot active"></span><span class="dot"></span><span class="dot"></span></div>
    </div>
    ''')

    # 头部
    html_lines.append(f'''
    <div class="header">
        <h1>{SITE_TITLE}</h1>
        <p>基于关键词自动分类 · 覆盖全国 / 广东省 / 广州市</p>
        <span class="badge">共 {len(entries)} 条新闻</span>
    </div>
    ''')

    # 搜索栏
    html_lines.append('''
    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="🔍 输入关键词搜索（如：城市更新）">
        <select id="regionFilter">
            <option value="">所有地域</option>
            <option value="全国">全国</option>
            <option value="广东省">广东省</option>
            <option value="广州市">广州市</option>
        </select>
        <button class="clear-btn" id="clearBtn">清除筛选</button>
    </div>
    ''')

    # 卡片网格，每条新闻加上 data-* 属性
    html_lines.append('<div class="grid" id="newsGrid">')
    region_order = ["全国", "广东省", "广州市"]
    # 为每个地域生成卡片，但卡片内列表项会包含数据属性，用于JS过滤
    for region in region_order:
        if region not in grouped:
            continue
        items = grouped[region]
        html_lines.append(f'<div class="card" data-region="{region}">')
        html_lines.append(f'<div class="category"><span class="icon">📌</span><h2>{region}</h2><span class="tag">{len(items)} 条</span></div>')
        html_lines.append('<ul class="news-list">')
        for item in items:
            title = html.escape(item['title'])
            summary = html.escape(item['summary'])
            link = item['link']
            pub = item['published'][:16] if len(item['published']) > 16 else item['published']
            keywords_str = ','.join(item['keywords'])  # 用于搜索
            region_str = item['region']
            tags_html = ''.join([f'<span class="keyword-tag">#{kw}</span>' for kw in item['keywords']])
            # 地域标签
            region_tag = f'<span class="region-tag">📍 {region_str}</span>'
            html_lines.append(f'''
            <li data-keywords="{keywords_str}" data-region="{region_str}" data-title="{title}">
                <a href="{link}" target="_blank">{title}</a>
                <div class="summary">{summary}</div>
                <div class="meta">
                    <span class="date">🕒 {pub}</span>
                    <span>{region_tag} {tags_html}</span>
                </div>
            </li>
            ''')
        html_lines.append('</ul>')
        html_lines.append('<div class="card-footer">📌 点击标题查看原文</div>')
        html_lines.append('</div>')
    html_lines.append('</div>')  # 结束 grid

    # 页脚
    html_lines.append(f'''
    <div class="footer">
        🤖 机器人每周一自动更新 · 数据来源于 RSS 聚合 · 仅供学习参考<br>
        <span style="font-size:0.8rem;">更新于 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
    </div>
    ''')

    html_lines.append('</div>')  # 结束 container

    # 返回顶部按钮 + 搜索过滤脚本
    html_lines.append('''
    <button class="back-to-top" id="backToTop" aria-label="回到顶部">↑</button>
    <script>
        (function() {
            // 过滤逻辑
            const searchInput = document.getElementById('searchInput');
            const regionFilter = document.getElementById('regionFilter');
            const clearBtn = document.getElementById('clearBtn');
            const allItems = document.querySelectorAll('.news-list li');
            const cards = document.querySelectorAll('.card');

            function filter() {
                const keyword = searchInput.value.trim().toLowerCase();
                const region = regionFilter.value;

                allItems.forEach(item => {
                    const title = item.getAttribute('data-title') || '';
                    const keywords = item.getAttribute('data-keywords') || '';
                    const itemRegion = item.getAttribute('data-region') || '';
                    const matchKeyword = keyword === '' || title.toLowerCase().includes(keyword) || keywords.toLowerCase().includes(keyword);
                    const matchRegion = region === '' || itemRegion === region;
                    item.style.display = (matchKeyword && matchRegion) ? '' : 'none';
                });

                // 更新每个卡片的计数
                cards.forEach(card => {
                    const list = card.querySelector('.news-list');
                    const items = list.querySelectorAll('li');
                    let visibleCount = 0;
                    items.forEach(li => { if (li.style.display !== 'none') visibleCount++; });
                    const tag = card.querySelector('.category .tag');
                    if (tag) tag.textContent = visibleCount + ' 条';
                });
            }

            searchInput.addEventListener('input', filter);
            regionFilter.addEventListener('change', filter);
            clearBtn.addEventListener('click', function() {
                searchInput.value = '';
                regionFilter.value = '';
                filter();
            });

            // 回到顶部
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
    print("稍等，机器人开始抓新闻了...")
    news = fetch_news()
    print(f"共抓取 {len(news)} 条新闻，正在排版...")
    generate_html(news)
    print("全部搞定！")
