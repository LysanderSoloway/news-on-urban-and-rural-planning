import feedparser
import datetime
import html
import re
from collections import defaultdict

# ---------- 奶奶，您想改新闻来源，就改这里面的网址 ----------
RSS_URLS = [
    "https://news.google.com/rss/search?q=城乡规划+国土空间&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=城市更新+老旧小区&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=乡村振兴+美丽乡村&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
]
SITE_TITLE = "🏠 城乡规划新闻周报（大字版）"
KEEP_DAYS = 7  # 只看最近7天的新闻
# ----------------------------------------------------------

def get_category(title, desc):
    text = (title + " " + desc).lower()
    if re.search(r'国土|空间规划|自然资|部|用地|红线', text):
        return "📐 国土空间规划"
    if re.search(r'城市更新|旧改|棚改|微更新|老旧小区', text):
        return "🏗️ 城市更新与建设"
    if re.search(r'乡村|振兴|农村|农业|宅基地', text):
        return "🌾 乡村振兴"
    if re.search(r'智慧城市|数字|数据|智能|互联网', text):
        return "💻 智慧城市"
    return "📰 综合新闻"

def fetch_news():
    all_entries = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                summary = entry.get('summary', entry.get('description', ''))
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = summary[:180] + "..."
                
                pub_time = entry.get('published', entry.get('updated', ''))
                if not pub_time:
                    continue
                    
                entry_data = {
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', '#'),
                    'summary': summary,
                    'published': pub_time,
                    'category': get_category(entry.get('title', ''), summary)
                }
                all_entries.append(entry_data)
        except Exception as e:
            print(f"抓取这个地址出了点小问题，但不影响: {url}")
            continue
    return all_entries

def generate_html(entries):
    entries.sort(key=lambda x: x['published'], reverse=True)
    
    categorized = defaultdict(list)
    for item in entries[:100]:
        categorized[item['category']].append(item)

    html_lines = []
    html_lines.append('<!DOCTYPE html><html><head><meta charset="UTF-8">')
    html_lines.append(f'<title>{SITE_TITLE}</title>')
    html_lines.append('''
    <style>
        body { background: #f5f5f5; font-family: "微软雅黑", sans-serif; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { font-size: 48px; color: #1a3c5e; text-align: center; border-bottom: 5px solid #1a3c5e; padding-bottom: 15px; }
        .date { text-align: center; font-size: 24px; color: #666; }
        .category { background: #ffffff; border-radius: 15px; padding: 20px; margin-top: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .cat-title { font-size: 36px; color: #fff; background: #2c6b9e; display: inline-block; padding: 5px 25px; border-radius: 30px; }
        .news-item { border-bottom: 2px dashed #ddd; padding: 20px 5px; }
        .news-item a { font-size: 28px; color: #003366; text-decoration: none; font-weight: bold; }
        .news-item a:hover { color: #ff6600; text-decoration: underline; }
        .summary { font-size: 22px; color: #333; background: #f9f9f9; padding: 15px; border-radius: 10px; line-height: 1.6; margin: 10px 0; }
        .meta { font-size: 18px; color: #888; }
        .footer { text-align: center; font-size: 22px; color: #aaa; margin-top: 40px; }
    </style>
    </head><body><div class="container">''')
    
    html_lines.append(f'<h1>{SITE_TITLE}</h1>')
    html_lines.append(f'<p class="date">📅 更新日期：{datetime.datetime.now().strftime("%Y年%m月%d日")}  (共{len(entries)}条新闻)</p>')

    if not categorized:
        html_lines.append('<p style="font-size:30px;">奶奶，今天还没抓到新闻，您点一下上面的"运行"按钮就好！</p>')
    else:
        for cat, items in categorized.items():
            html_lines.append(f'<div class="category"><div class="cat-title">{cat} ({len(items)})</div>')
            for item in items:
                title = html.escape(item['title'])
                summary = html.escape(item['summary'])
                link = item['link']
                pub = item['published'][:16] if len(item['published']) > 16 else item['published']
                html_lines.append(f'''
                <div class="news-item">
                    <a href="{link}" target="_blank">🔹 {title}</a>
                    <div class="summary">📖 {summary}</div>
                    <div class="meta">🕒 {pub}</div>
                </div>
                ''')
            html_lines.append('</div>')
    
    html_lines.append(f'<div class="footer">🤖 机器人每周一自动更新 · 祝奶奶身体健康！</div>')
    html_lines.append('</div></body></html>')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    print("网页生成成功啦！")

if __name__ == "__main__":
    print("奶奶稍等，机器人开始抓新闻了...")
    news = fetch_news()
    print(f"抓到了 {len(news)} 条新闻，正在排版...")
    generate_html(news)
    print("全部搞定！")
