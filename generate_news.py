import feedparser
import datetime
import html
import re
from collections import defaultdict

# ===================== 配置区（奶奶可以自己改）=====================
RSS_URLS = [
    "https://news.google.com/rss/search?q=城乡规划+国土空间&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=城市更新+老旧小区&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=乡村振兴+美丽乡村&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=城市体检+安全韧性&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=智能建造+数智孪生&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
]

# 您定义的 12 个关键词
KEYWORDS = [
    "存量提质增效", "城市更新十五五规划", "人本更新", "城市体检",
    "安全韧性", "四好建设", "城乡融合", "新质生产力",
    "临时使用", "规划转型", "智能建造", "数智孪生"
]

SITE_TITLE = "🏠 城乡规划新闻周报（关键词分类·大字版）"
# ================================================================

def extract_region(text):
    """根据新闻内容判断地域：全国 / 广东省 / 广州市"""
    text = text.lower()
    if re.search(r'广州|越秀|天河|海珠|荔湾|白云|黄埔|番禺|花都|南沙|从化|增城', text):
        return "📍 广州市"
    elif re.search(r'广东|深圳|东莞|佛山|珠海|中山|惠州|江门|肇庆|汕头|湛江', text):
        return "📍 广东省"
    else:
        return "📍 全国"

def match_keywords(text):
    """匹配新闻内容中含有的关键词，返回匹配到的关键词列表"""
    matched = []
    for kw in KEYWORDS:
        # 特殊处理“城市更新十五五规划”可能写作“城市更新‘十五五’规划”
        if kw == "城市更新十五五规划":
            if re.search(r'城市更新.*?十五五|十五五.*?城市更新', text):
                matched.append(kw)
        elif kw in text:
            matched.append(kw)
    return matched if matched else ["📌 其他"]

def fetch_news():
    all_entries = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # 提取标题和正文
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                full_text = title + " " + summary
                # 去除HTML标签
                summary_clean = re.sub(r'<[^>]+>', '', summary)
                summary_clean = summary_clean[:180] + "..." if len(summary_clean) > 180 else summary_clean
                
                pub_time = entry.get('published', entry.get('updated', ''))
                if not pub_time:
                    continue
                
                # 地域分类
                region = extract_region(full_text)
                # 关键词匹配
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
    # 按时间倒序排序（最新的在前）
    entries.sort(key=lambda x: x['published'], reverse=True)
    # 按地域分组
    grouped_by_region = defaultdict(list)
    for item in entries[:150]:  # 取最新150条
        grouped_by_region[item['region']].append(item)

    html_lines = []
    html_lines.append('<!DOCTYPE html><html><head><meta charset="UTF-8">')
    html_lines.append(f'<title>{SITE_TITLE}</title>')
    html_lines.append('''
    <style>
        body { background: #f0f4f8; font-family: "微软雅黑", sans-serif; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 48px; color: #1a3c5e; text-align: center; border-bottom: 5px solid #1a3c5e; padding-bottom: 15px; }
        .date { text-align: center; font-size: 24px; color: #666; margin-bottom: 30px; }
        .region-block { background: #ffffff; border-radius: 15px; padding: 20px; margin-bottom: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .region-title { font-size: 36px; color: #fff; background: #2c6b9e; display: inline-block; padding: 5px 30px; border-radius: 30px; }
        .news-item { border-bottom: 2px dashed #ddd; padding: 18px 5px; }
        .news-item a { font-size: 26px; color: #003366; text-decoration: none; font-weight: bold; }
        .news-item a:hover { color: #ff6600; text-decoration: underline; }
        .summary { font-size: 20px; color: #333; background: #f9f9fc; padding: 12px 18px; border-radius: 10px; line-height: 1.6; margin: 8px 0; }
        .meta { font-size: 18px; color: #888; margin-top: 5px; }
        .keyword-tag { display: inline-block; background: #e6f0fa; color: #1a3c5e; padding: 2px 14px; border-radius: 20px; font-size: 18px; margin-right: 8px; }
        .footer { text-align: center; font-size: 22px; color: #aaa; margin-top: 40px; padding-top: 20px; border-top: 2px solid #ddd; }
    </style>
    </head><body><div class="container">''')

    html_lines.append(f'<h1>{SITE_TITLE}</h1>')
    html_lines.append(f'<p class="date">📅 更新日期：{datetime.datetime.now().strftime("%Y年%m月%d日")}  (共{len(entries)}条新闻)</p>')

    if not grouped_by_region:
        html_lines.append('<p style="font-size:30px;">奶奶，暂时没有抓到新闻，请稍后手动运行一次。</p>')
    else:
        # 按地域顺序展示：全国 → 广东省 → 广州市
        region_order = ["📍 全国", "📍 广东省", "📍 广州市"]
        for region in region_order:
            if region not in grouped_by_region:
                continue
            items = grouped_by_region[region]
            html_lines.append(f'<div class="region-block"><div class="region-title">{region} ({len(items)})</div>')
            for item in items:
                title = html.escape(item['title'])
                summary = html.escape(item['summary'])
                link = item['link']
                pub = item['published'][:16] if len(item['published']) > 16 else item['published']
                # 关键词标签
                tags = ''.join([f'<span class="keyword-tag">#{kw}</span>' for kw in item['keywords']])
                html_lines.append(f'''
                <div class="news-item">
                    <a href="{link}" target="_blank">🔹 {title}</a>
                    <div class="summary">📖 {summary}</div>
                    <div class="meta">🕒 {pub}  {tags}</div>
                </div>
                ''')
            html_lines.append('</div>')

    html_lines.append(f'<div class="footer">🤖 机器人每周一自动更新 · 关键词精准分类 · 祝奶奶身体健康！</div>')
    html_lines.append('</div></body></html>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    print("网页生成成功！")

if __name__ == "__main__":
    print("奶奶稍等，机器人开始抓新闻了...")
    news = fetch_news()
    print(f"共抓取 {len(news)} 条新闻，正在排版...")
    generate_html(news)
    print("全部搞定！")
