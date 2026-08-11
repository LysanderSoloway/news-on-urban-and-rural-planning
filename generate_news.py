import feedparser
import datetime
import html
import re
import json
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

KEYWORD_ALIAS = {
    "存量提质增效": "存量提质增效",
    "城市更新十五五规划": "城市更新（十五五）规划",
    "人本更新": "人本更新",
    "城市体检": "城市体检",
    "安全韧性": "安全韧性",
    "四好建设": "好房子·好小区·好社区·好城区",
    "城乡融合": "城乡融合",
    "新质生产力": "新质生产力",
    "临时使用": "临时使用",
    "规划转型": "规划转型",
    "智能建造": "智能建造",
    "数智孪生": "数智孪生"
}

SITE_TITLE = "城乡规划 · 十大热点新闻聚合"
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
    return matched

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
                if not keywords:
                    continue
                source = entry.get('source', {}).get('title', '未知来源')
                date_str = pub_time[:10] if len(pub_time) >= 10 else pub_time
                all_entries.append({
                    'title': title,
                    'url': entry.get('link', '#'),
                    'source': source,
                    'date': date_str,
                    'region': region,
                    'keywords': keywords
                })
        except Exception as e:
            print(f"抓取 {url} 出错：{e}")
            continue
    return all_entries

# ===================== 静态新闻数据 =====================
STATIC_DATA = {
    "存量提质增效": [
        {"title": "年内出台政策近百条 城市更新按下加速键", "url": "https://stcn.com/article/detail/4036338.html", "source": "证券时报", "date": "2026-07-23"},
        {"title": "专家解读：加快适应房地产存量时代的到来", "url": "https://www.chinajsb.cn/html/202607/17/58447.html", "source": "中国建设新闻网", "date": "2026-07-17"},
        {"title": "城市更新叩响现代化人民城市之门（发改委）", "url": "https://www.ndrc.gov.cn/wsdwhfz/202606/t20260601_1405594.html", "source": "国家发改委", "date": "2026-06-01"},
        {"title": "培育壮大城市发展新动能", "url": "https://jxrb.jxwmw.cn/system/2026/08/02/031206821.shtml", "source": "江西日报", "date": "2026-08-02"},
        {"title": "2026年上半年城市更新盘点：政策闭环成型，行业转向存量长效运营", "url": "https://stcn.com/article/detail/4028015.html", "source": "每日经济新闻", "date": "2026-07-20"},
        {"title": "我市推出2026版存量盘活升级政策（天津）", "url": "https://www.tj.gov.cn/sy/tjxw/202608/t20260803_7345723.html", "source": "天津市人民政府", "date": "2026-08-03"},
        {"title": "激活存量资源潜力 赋能城市高质量发展（吉林）", "url": "https://fzzx.jl.gov.cn/yjcg/202601/t20260104_9387911.html", "source": "吉林省发改委", "date": "2026-01-04"},
        {"title": "北京发布2026年度建设用地供应计划 首次单列城市更新计划指标", "url": "https://bj.people.com.cn", "source": "人民网-北京频道", "date": "2026-01-20"},
        {"title": "深化控规改革 激活城市更新 北京推动好房子建设向好街区跃升", "url": "https://www.beijing.gov.cn", "source": "北京市人民政府", "date": "2026-08-02"},
        {"title": "武汉出台城市更新十五五规划 优先改造600个以上老旧小区", "url": "https://www.changjiangtimes.com", "source": "长江时报", "date": "2026-08-03"},
        {"title": "广州花都裕辉·时尚智造产业园进入试投产阶段", "url": "https://www.cnr.cn/gd/guangdonglueying/20260710/t20260710_527700697.shtml", "source": "央广网", "date": "2026-07-10"},
        {"title": "广州花都：自主更新赋能现代化人民城市建设", "url": "https://zfcj.gz.gov.cn/gkmlpt/content/10/10455/post_10455282.html", "source": "广州市住建局", "date": "2025-09-19"},
        {"title": "广州天河体育中心小柱墩大提升 沉睡绿地变街角乐园", "url": "http://www.gz.gov.cn/zwfw/zxfw/ggfw/content/mpost_10404730.html", "source": "广州市人民政府", "date": "2025-08-18"},
        {"title": "市场化盘活村存量土地 焕新低效园区（广州）", "url": "http://www.cnr.cn/gd/fxgz/20250910/t20250910_527355768.shtml", "source": "央广网", "date": "2025-09-10"},
        {"title": "安踏晋江智慧产业园：并宗提容，低效用地再开发跑出加速度", "url": "https://fj.people.cn", "source": "人民网-福建频道", "date": "2026-08-04"},
        {"title": "自然资源部：盘活存量土地 以较小资源消耗支撑高质量发展", "url": "https://finance.people.com.cn", "source": "人民网", "date": "2026-06-25"},
        {"title": "幼儿园改造成养老服务综合体，武汉让沉睡空间变身民生载体", "url": "https://zrzyt.hubei.gov.cn", "source": "湖北省自然资源厅", "date": "2026-07-31"},
        {"title": "一条锦鲤游进老厂房 广埠屯科创园区冲刺10月开园", "url": "https://tc.wuhan.gov.cn", "source": "武汉市人民政府", "date": "2026-08-04"},
        {"title": "存量时代规划和土地政策必须从管住走向激活", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "房地产正式迈入存量发展时代，二手房成交占比超50%", "url": "https://www.chinajsb.cn/html/202607/17/58447.html", "source": "中国建设新闻网", "date": "2026-07-17"},
        {"title": "城市更新聚焦23项重点任务（权威发布）", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "新时期城市更新的核心导向", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "十五五高质量推进城市更新有了路线图任务书", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "张学冬：城市更新进入系统落地期，要从物本转向人本", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "城市体检为城市把脉开方", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "如何高质量推进城市更新？专家：从物本更新转向人本更新", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "广州：深耕储备用地精细管理 盘活存量资源提质增效", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "国务院政策例行吹风会文字实录", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "广州创新打造边角地+新能源土地临时利用样板", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "城市更新存量盘活从管住走向激活", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "新增建设用地原则上不用于经营性房地产开发", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "盘活存量土地倒逼地方发展转向存量挖潜", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "澎湃新闻", "date": "2026-07-06"},
        {"title": "行业从投资驱动转向存量长效运营", "url": "https://stcn.com/article/detail/4028015.html", "source": "每日经济新闻", "date": "2026-07-20"},
        {"title": "广州常态化推进储备地块规范化围蔽整治", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "广州严格落实净地出让标准，实现企业拿地即开工", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "广州探索三资盘活利用新机制", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "城市更新专项中央预算内投资970亿元惠及800万户", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "地下管网建设改造超长期特别国债安排1600亿元", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "中央财政支持50个重点城市先行先试", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "广州创新打造边角地+新能源土地临时利用样板（续）", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "北京丰台发布八大城市更新场景，从拆改留到精提质", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "亚洲最大鞋城转型智慧办公地标，京印国际中心出租率达90%", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "南中轴9.7万平方米存量楼宇全面盘活，剥离传统服装商贸", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "中车二七厂百年工业遗存焕新，布局轨道交通与空天信息产业", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "丰台区创新城市更新先锋工作营机制", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "丰台落地同编共审与两统一、一分散实施路径", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "北京丰台发布危楼改建、智能建造、产业升级等八大场景", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "长辛店老镇微更新激活千年文脉，获评市级最佳实践", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "京印国际中心智能建造实现暖通空调节能35.38%", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "丰台开阳里三区38户危楼居民迁入成套新居", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "丰台区城市更新服务专窗开通，三师团队全周期服务", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "丰台区将城市更新场景建设纳入全域场景化发展核心体系", "url": "https://baijiahao.baidu.com/s?id=1872593511727442805", "source": "潮新闻", "date": "2026-08-04"},
        {"title": "从点状实践到系统推进 湖北城市更新加速推进", "url": "http://www.jmtv.com.cn/folder48/folder49/folder59/2026-08-06/zHecGuC92OAj1ToZ.html", "source": "长江云新闻", "date": "2026-08-06"},
        {"title": "十四五时期各地累计改造城镇老旧小区24万多个，惠及约1.1亿人", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "十五五将新开工改造城镇老旧小区11.5万个", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "城市发展正从大规模增量扩张转向存量提质增效", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "广州越秀区十五五启动新一轮4个老旧小区成片连片改造", "url": "https://huacheng.gz-cmc.com/pages/2026/08/06/9a4249471b364f0dbe33a807ecd2a287.html", "source": "广州日报新花城", "date": "2026-08-06"},
        {"title": "北京华威北里老旧小区引入物业服务，收缴率达96%", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "上海黄浦区市民新村从老旧破到新绿美改造", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "城市更新领域首部国家级专项规划发布，聚焦存量资源盘活", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "湖北武汉硚口皮子街南洋1916老旧片区系统化更新", "url": "http://www.jmtv.com.cn/folder48/folder49/folder59/2026-08-06/zHecGuC92OAj1ToZ.html", "source": "长江云新闻", "date": "2026-08-06"},
        {"title": "广州推进百千万工程，盘活城中村与低效用地", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"}
    ],
    "城市更新十五五规划": [
        {"title": "国务院关于印发《城市更新十五五规划》的通知", "url": "https://www.gov.cn/zhengce/content/202605/content_7070539.htm", "source": "中国政府网", "date": "2026-05-15"},
        {"title": "十五五高质量推进城市更新有了路线图任务书", "url": "https://www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "国务院政策例行吹风会文字实录（2026年6月8日）", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "国新办", "date": "2026-06-08"},
        {"title": "四部门解读《城市更新十五五规划》", "url": "https://www.gov.cn/zhengce/202606/content_7071502.htm", "source": "新华社", "date": "2026-06-08"},
        {"title": "国新办举行国务院政策例行吹风会", "url": "http://www.scio.gov.cn/live/2026/38728/tw/index_m.html", "source": "国新网", "date": "2026-06-08"},
        {"title": "城市更新十五五规划出炉 将带动十万亿元级投资", "url": "https://finance.cctv.com/2026/05/29/ARTI1cAHuebbYX38Lna97haL260529.shtml", "source": "央视网", "date": "2026-05-29"},
        {"title": "中国发布丨11.5万个老旧小区将开工改造！", "url": "http://news.china.com.cn/2026-06/08/content_118536835.htm", "source": "中国网", "date": "2026-06-08"},
        {"title": "城市更新聚焦23项重点任务（权威发布）", "url": "https://gd.people.com.cn", "source": "人民网", "date": "2026-06-09"},
        {"title": "做好做实城市更新潜绩", "url": "http://theory.people.com.cn/BIG5/n1/2026/0609/c40531-40736439.html", "source": "光明日报", "date": "2026-06-09"},
        {"title": "老街区、老厂区要大变样了", "url": "http://paper.people.com.cn/rmrbhwb/pc/content/202606/30/content_30165771.html", "source": "人民日报海外版", "date": "2026-06-30"},
        {"title": "广州市白云区城市更新十五五规划（采购公告）", "url": "https://www.ccgp.gov.cn", "source": "中国政府采购网", "date": "2026-07-01"},
        {"title": "《城市更新十五五规划》解读：有哪些重要变化？", "url": "http://www.sdyanbao.com/detail/972524", "source": "中银证券", "date": "2026-06-05"},
        {"title": "年内出台政策近百条 城市更新按下加速键", "url": "https://stcn.com/article/detail/4036338.html", "source": "21世纪经济报道", "date": "2026-07-23"},
        {"title": "城市更新十五五规划三大亮点：投融资体系、定量目标、四好建设", "url": "http://www.sdyanbao.com/detail/972524", "source": "中银证券", "date": "2026-06-05"},
        {"title": "十五五城市更新核心KPI：危旧房改造量翻倍", "url": "http://www.sdyanbao.com/detail/972524", "source": "中银证券", "date": "2026-06-05"},
        {"title": "地下管网改造77万公里，预计带动5万亿元投资", "url": "http://www.sdyanbao.com/detail/972524", "source": "国家发改委", "date": "2026-05-22"},
        {"title": "城市更新投资总额十五五期间不低于16万亿元", "url": "https://stcn.com/article/detail/4036338.html", "source": "住建部", "date": "2026-06-24"},
        {"title": "武汉出台《关于支持城市更新的若干政策措施（第三批）》", "url": "https://stcn.com/article/detail/4036338.html", "source": "武汉市政府", "date": "2026-07-15"},
        {"title": "《福建省十五五城市更新规划》印发", "url": "https://stcn.com/article/detail/4036338.html", "source": "福建省政府", "date": "2026-07-15"},
        {"title": "中央财政支持实施城市更新行动，2026年资金已下达", "url": "https://stcn.com/article/detail/4036338.html", "source": "财政部、住建部", "date": "2026-04-15"},
        {"title": "城市更新聚焦23项重点任务（权威发布·第二批）", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "十五五高质量推进城市更新有了路线图任务书", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "建设好房子，改造老旧小区……城市更新聚焦23项重点任务", "url": "https://news.cctv.com/2026/06/09/ARTIVTA7IwtfkcedtBblRWbG260609.shtml", "source": "央视网", "date": "2026-06-09"},
        {"title": "规划提出10项主要指标、23项重点任务、7方面政策举措", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "规划部署6方面重点任务：培育新动能、营造高品质生活空间等", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "规划提出14项重大工程和行动", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "到2030年城市更新行动取得重要进展", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "城镇危旧房改造50万套、老旧小区改造11.5万个", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "城中村改造4000个、地下管网改造36.5万公里", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "应急避难场所改造5万个、房屋数字化率95%以上", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "城市更新领域第一部国家级专项规划", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "中央财政支持50个重点城市先行先试", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "城市更新专项中央预算内投资970亿元", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "地下管网建设改造超长期特别国债1600亿元", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "297个地级及以上城市开展城市体检", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "十四五累计改造老旧小区24万个", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "加装电梯12.9万部、增设施6.4万个", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "城市地下管网建设改造约77万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "燃气管网20万公里、排水管网17.5万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "首部国家级城市更新专项规划发布，10项指标聚焦群众急难愁盼", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "五大亮点看城市更新施工图", "url": "http://jiwei.guiyang.gov.cn/xwhc/yw/202606/t20260615_90523470.html", "source": "中央纪委国家监委网站", "date": "2026-06-08"},
        {"title": "规划提出10项指标、23项重点任务、7方面政策举措", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "规划部署6方面重点任务：创新、宜居、美丽、韧性、文明、智慧", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "规划通过专栏列出好房子建设等14项重大工程", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "10项指标包括危旧房改造、老旧小区改造、地下管网改造等", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "规划部署三类工程：民生工程、发展工程、安全工程", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "构建中央统筹、省负总责、城市抓落实工作格局", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "规划坚持尽力而为、量力而行，做到可感知、可量化、可评价", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "规划聚焦为民、便民、安民，解决群众急难愁盼", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "中央财政支持50个重点城市先行先试城市更新", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "城市更新专项中央预算内投资970亿元惠及800万户", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "国务院印发《城市更新十五五规划》，首部国家级专项规划", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "规划提出10项主要指标、23项重点任务、7方面政策举措", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "规划部署6方面重点任务：创新、宜居、美丽、韧性、文明、智慧", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "五大亮点看城市更新施工图", "url": "http://jiwei.guiyang.gov.cn/xwhc/yw/202606/t20260615_90523470.html", "source": "中央纪委国家监委网站", "date": "2026-06-08"},
        {"title": "规划设定2030年和2035年两个阶段重要目标", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "规划部署三类工程：民生工程、发展工程、安全工程", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/jdzc/202606/content_7071440.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "规划提出好房子建设等14项重大工程和行动", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "到2030年城市更新行动取得重要进展，城市开发建设方式转型初见成效", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "中央财政连续3年累计支持50个重点城市先行先试", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "构建中央统筹、省负总责、城市抓落实工作格局", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"}
    ],
    "人本更新": [
        {"title": "如何高质量推进城市更新？专家：从物本更新转向人本更新", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "壹时评：把人写进城市更新的每一个细节", "url": "https://m.haiwainet.cn/middle/3544276/2026/0723/content_32970008_1.html", "source": "人民网", "date": "2026-07-23"},
        {"title": "张学冬：城市更新进入系统落地期，要从物本转向人本", "url": "https://beijing.creb.com.cn", "source": "北京商报", "date": "2026-07-06"},
        {"title": "新时期城市更新的核心导向", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "新思想引领新征程丨高质量推进城市更新 建设现代化人民城市", "url": "https://china.cnr.cn/news/sz/20260802/t20260802_527742488.shtml", "source": "央广网", "date": "2026-08-02"},
        {"title": "接住群众期盼，城市更新当多些细腻巧思", "url": "https://www.ctdsb.net/c1734_202608/2820757.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "多考虑人的尺度，城市更新不能浮于表面洗把脸", "url": "https://www.peopleapp.com/column/30052593790-500007585613", "source": "人民日报", "date": "2026-07-08"},
        {"title": "丈量人的尺度", "url": "https://news.dayoo.com/guangzhou/202607/09/153828_54977720.htm", "source": "人民日报", "date": "2026-07-09"},
        {"title": "西安，正为你而改变", "url": "http://xa.wenming.cn/wmchuanjianxin/202607/t20260716_9300430.html", "source": "西安文明网", "date": "2026-07-16"},
        {"title": "聚焦于人的城市更新，就是创新城市", "url": "https://www.huxiu.com/article/4865216.html", "source": "虎嗅", "date": "2026-06-08"},
        {"title": "城市更新的幸福密码藏在烟火与新意里", "url": "https://yhcb.eyh.cn/html/2026-04/08/content_82167_3313444.htm", "source": "余杭时报", "date": "2026-04-08"},
        {"title": "石晓冬：城市公共投资要从物质形态转向服务形态", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "城市更新从物本全面转向人本", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "中国房地产报", "date": "2026-07-05"},
        {"title": "人民城市理念在中华大地上持续勾画出幸福之城", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网-人民日报", "date": "2026-08-03"},
        {"title": "城市更新要全面践行人民城市理念", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "坚持问需于民、问计于民、问效于民", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "城市更新要做深做细做实", "url": "https://www.peopleapp.com/column/30052593790-500007585613", "source": "人民日报", "date": "2026-07-08"},
        {"title": "基层治理要让居民从旁观者变成参与者", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "城市体检民生指标权重提升，回归以人为本", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "高质量推进城市更新 建设现代化人民城市", "url": "https://china.cnr.cn/news/sz/20260802/t20260802_527742488.shtml", "source": "央广网", "date": "2026-08-02"},
        {"title": "张学冬：城市更新进入系统落地期，要从物本转向人本（第二批）", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "如何高质量推进城市更新？专家：从物本更新转向人本更新（第二批）", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "城市更新从物本更新全面转向人本更新", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "城市的核心是人，根本目的是让人民生活更美好", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "石晓冬：城市公共投资要从物质形态转向服务形态（第二批）", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "人民城市人民建，人民城市为人民理念贯穿更新全过程", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "城市更新核心目标是提升安全韧性、延续文脉、优化民生品质", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "坚持问需于民、问计于民、问效于民（第二批）", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "城市更新要做深做细做实（第二批）", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "从政府想做什么到群众需要什么的转变", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "无体检，不更新让城市体检成为前置条件", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新算的是民生账、安全账", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "四好体系塑造高品质生活", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "推进一刻钟生活圈建设", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新要全面践行人民城市理念（第二批）", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "把民生获得感作为最终标尺", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新不仅是物理空间重塑，更是城市治理能力提升", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "城市更新从试点探索走向系统落地的关键一年", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "存量提质、精细治理、长效运行成新时代核心主线", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "2026年是城市更新从试点探索走向系统落地的关键一年", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "存量提质、精细治理、长效运行成新时代城市建设的核心主线", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "城市更新核心目标是提升安全韧性、延续历史文脉、优化民生品质", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "人民城市人民建，人民城市为人民贯穿城市更新全过程", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "城市更新不是短期改造工程，而是重塑城市功能的长期事业", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "城市更新从试点探索走向系统落地的关键一年", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "张学冬：城市更新从物本全面转向人本", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "石晓冬：城市公共投资要从物质形态转向服务形态和福利形态", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785092520427", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "城市的核心是人，根本目的是让人民生活更美好", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "坚持问需于民、问计于民、问效于民，做深做细做实城市更新", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "上海华漕保障房项目层高3米+双阳台，打造好房子", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "《四川省好住房评价标准》实施，全国首个地方标准", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "天津中新生态城第四社区：5分钟生活圈", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "好社区是能承载生活温度的空间，从居住场所到生活乐园", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "完整社区建设从试点转向扩面提质，5000个社区实施建设改造", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "清华大学边兰春：完整社区建设需健全多元投融资方式", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "2026年完整社区建设工作重心从试点转向扩面提质", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "越秀区十五五将打造2个省级未来社区试点", "url": "https://huacheng.gz-cmc.com/pages/2026/08/06/9a4249471b364f0dbe33a807ecd2a287.html", "source": "广州日报新花城", "date": "2026-08-06"}
    ],
    "城市体检": [
        {"title": "地级及以上城市、县级市今年将全面开展城市体检", "url": "https://paper.people.com.cn/rmrb/pc/content/202605/17/content_30157305.html", "source": "人民日报", "date": "2026-05-17"},
        {"title": "住房城乡建设部召开2026年城市体检工作部署视频会", "url": "https://zjt.fj.gov.cn/xxgk/gzdt/bmdt/202605/t20260518_7149183.htm", "source": "福建省住建厅", "date": "2026-05-18"},
        {"title": "住房城乡建设部：一体化推进城市体检与城市更新", "url": "https://www.nmg.gov.cn/zwyw/qgyw/202605/t20260518_2903809.html", "source": "内蒙古政府网", "date": "2026-05-18"},
        {"title": "高质量推进城市更新 住建部再部署城市体检", "url": "http://www.fangchan.com/news/6/2026-05-18/7461953880189112964.html", "source": "中房网", "date": "2026-05-18"},
        {"title": "无体检不更新，全国设市城市迎健康大考", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "扩围提质，你的城市体检了吗", "url": "http://mrdx.cn/content/20260527/Articel03004NR.htm", "source": "新华每日电讯", "date": "2026-05-27"},
        {"title": "城市体检为城市把脉开方", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "给城市做个精密体检（深阅读）", "url": "https://cpc.people.com.cn/BIG5/n1/2026/0511/c64387-40717347.html", "source": "人民网", "date": "2026-05-11"},
        {"title": "海南启动2026年城市（县城）体检", "url": "https://www.hainan.gov.cn/hainan/5309/202605/3011196513034244990790b96191e0c3.shtml", "source": "海南省政府网", "date": "2026-05-20"},
        {"title": "鹤山市全面开展2026年度城市体检工作", "url": "http://www.jiangmen.gov.cn/home/sqdt/hszx/content/post_3519319.html", "source": "江门市政府网", "date": "2026-06-15"},
        {"title": "城市体检搭建住房—小区—街区—城区四维诊断体系", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "先体检后更新、无体检不更新成为刚性原则", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "城市体检从宏观经济导向转向民生幸福导向", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "北京劲松街道：体检与接诉即办深度融合", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "江苏连云港：体检结果支撑200个项目库", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "河北涉县：县级城市体检先行者", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "科技赋能城市体检：天空地一体化融合感知", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "城市体检人才缺口大，城市医生培养加速", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "北京科技大学开设工程诊治本科专业", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "城市体检推动从治已病转向治未病", "url": "https://paper.people.com.cn/zgcsb/pc/content/202605/25/content_30158979.html", "source": "中国城市报", "date": "2026-05-25"},
        {"title": "城市体检为城市把脉开方（第二批）", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "住房城乡建设部召开2026年城市体检工作部署视频会（第二批）", "url": "https://www.mohurdic.org.cn:10443/xw/jsyw/art/2026/art_758494918.html", "source": "住建部信息中心", "date": "2026-05-15"},
        {"title": "城市体检为城市更新基础，297个地级市开展体检", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "先体检、后更新、无体检、不更新成共识", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "住房、小区、街区、城区四个维度体检全覆盖", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "呼和浩特增设32项地方特色体检指标", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "邵阳构建重点更新片区体检指标体系", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "广州南沙开展青年发展型城市专项体检", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "保定开展城中村腾空土地改造专项体检", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "山西通过立法明确城市体检与更新规划衔接机制", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "赣州以体检结果形成项目建议清单", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "石家庄建立闲置空间即查即改转化机制", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "北京中关村构建多部门联动街道级体检机制", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "佛山建立跨年度问题整改跟踪台账", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "范嗣斌：用好评检问题清单和整治建议清单", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "城市体检从查病因到治顽疾", "url": "https://www.workercn.cn/c/2026-08-03/8861362.shtml", "source": "经济日报", "date": "2026-08-03"},
        {"title": "2026年城市体检工作部署视频会召开", "url": "https://www.mohurdic.org.cn:10443/xw/jsyw/art/2026/art_758494918.html", "source": "住建部信息中心", "date": "2026-05-15"},
        {"title": "总结交流2025年城市体检工作成效", "url": "https://www.mohurdic.org.cn:10443/xw/jsyw/art/2026/art_758494918.html", "source": "住建部信息中心", "date": "2026-05-15"},
        {"title": "设市城市全面开展城市体检工作", "url": "https://www.mohurdic.org.cn:10443/xw/jsyw/art/2026/art_758494918.html", "source": "住建部信息中心", "date": "2026-05-15"},
        {"title": "健全发现问题、解决问题、评估效果、巩固提升工作机制", "url": "https://www.mohurdic.org.cn:10443/xw/jsyw/art/2026/art_758494918.html", "source": "住建部信息中心", "date": "2026-05-15"},
        {"title": "地级及以上城市、县级市今年全面开展城市体检工作", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "住房城乡建设部：一体化推进城市体检与城市更新", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "住建部召开2026年城市体检工作部署视频会", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "坚持先体检后更新、无体检不更新", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "加快实现住房、小区、街区、城区四个维度体检全覆盖", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "去年全国297个地级市和152个县级市开展城市体检", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "城市体检以城市高质量发展为目标，建立指标体系", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "城市体检运用统计、大数据分析和社会调查等方法", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "城市体检促进城市治理体系和治理能力现代化", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "各地要结合城市更新重点任务因地制宜开展专项体检", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "健全发现问题、解决问题、评估效果、巩固提升的工作机制", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "城市体查找群众急难愁盼问题", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "住房城乡建设部：设市城市全面开展城市体检工作", "url": "http://www.xinhuanet.com/government/20260518/c0a7d3a6f30445d984bf6fbe48aef2e4/c.html", "source": "新华网", "date": "2026-05-18"},
        {"title": "城市体检对城市人居环境质量进行定期分析评估", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "城市体检反馈城市建设工作成效", "url": "http://jl.people.com.cn/BIG5/n2/2026/0517/c349771-41582398.html", "source": "人民网", "date": "2026-05-17"},
        {"title": "定期体检让城市更健康：今年地级及以上城市和县级市全面开展", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "坚持先体检后更新、无体检不更新", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "加快实现住房、小区、街区、城区四个维度全覆盖", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "城市体检搭建发现问题、解决问题、评估效果、巩固提升闭环", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "常态化城市体检紧盯群众急难愁盼的民生痛点", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "城市体检帮助持续优化人居环境、完善城市功能", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "《城市更新十五五规划》提出10项指标，含危旧房改造、老旧小区改造等", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "住房城乡建设部明确今年地级及以上城市和县级市全面开展城市体检", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "城市体检运用统计、大数据分析和社会调查等方法", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"},
        {"title": "体检结果与城市更新规划深度衔接", "url": "http://lw.news.cn/20260526/98590939f3fd4d0eb257781f46aca7fb/c.html", "source": "瞭望", "date": "2026-05-26"}
    ],
    "安全韧性": [
        {"title": "【新闻随笔】让城市安全治理既有精度又有温度", "url": "https://epaper.gmw.cn/gmrb/html/content/202606/08/content_15990.html", "source": "光明日报", "date": "2026-06-08"},
        {"title": "抓住更新契机增强城市安全韧性", "url": "http://theory.people.com.cn/BIG5/n1/2026/0601/c40531-40731225.html", "source": "经济日报", "date": "2026-06-01"},
        {"title": "专家解读 | 彭翀：安全韧性贯穿规划的新使命、新空间、新技术、新机制", "url": "https://www.thepaper.cn/newsDetail_forward_33638478", "source": "澎湃新闻", "date": "2026-07-22"},
        {"title": "专家解读·城市更新｜骆建云：增强城市安全韧性，擘画城市更新十五五新篇章", "url": "http://jst.sc.gov.cn/scjst/c101448/2026/6/22/b4157ff369a8408e85623d5a4bbc2626.shtml", "source": "中国建设新闻网", "date": "2026-06-22"},
        {"title": "专家解读·城市更新｜吕红亮：筑牢城市安全根基 系统提升城市韧性水平", "url": "http://www.chinajsb.cn/html/202606/04/57386.html", "source": "中国建设新闻网", "date": "2026-06-04"},
        {"title": "打造韧性安全城市上海方案：一张蓝图、一座克隆岛、一批吹哨人", "url": "https://nw.eastday.com/self/yw/20260716/472c45ce04a64c2d9034d8c5ea3c166d.html", "source": "上观新闻", "date": "2026-07-16"},
        {"title": "山城重庆：走出韧性城市建设新路径", "url": "https://www.cqrd.gov.cn/web/article/1517144792143499264/web/content_1517144792143499264.html", "source": "民主与法制周刊", "date": "2026-06-18"},
        {"title": "杨浦区人大社会委听取《杨浦区韧性安全城区建设十五五规划》", "url": "https://www.shanghai.gov.cn/nw15343/20260609/c6cffb5a32bb4abf9664af33b123278d.html", "source": "上海市政府网", "date": "2026-06-08"},
        {"title": "广东省印发《推进新型城市基础设施建设打造韧性城市行动方案（2025—2027年）》", "url": "https://zfcxjst.gd.gov.cn/gkmlpt/content/4/4842/post_4842956.html", "source": "广东省住建厅", "date": "2026-01-14"},
        {"title": "全国首创 北京构建韧性城市建设标准体系", "url": "https://bj.people.com.cn", "source": "人民网-北京频道", "date": "2026-04-02"},
        {"title": "中外专家在沪共探复合危机时代城市韧性建设路径", "url": "http://www.sh.chinanews.com.cn/shms/2026-07-05/147558.shtml", "source": "中新社上海", "date": "2026-07-05"},
        {"title": "第十届城市安全与防灾规划年度论坛成功举办", "url": "https://www.planning.org.cn", "source": "中国城市规划学会", "date": "2026-06-11"},
        {"title": "秦海翔出席2026年金砖国家城镇化部长级论坛", "url": "https://www.mohurd.gov.cn", "source": "住建部", "date": "2026-06-15"},
        {"title": "合肥：给城市装安全网——城市生命线安全工程", "url": "https://lw.news.cn/20260610/2e88b292332942c99bb7f880c69b9f50/c.html", "source": "瞭望", "date": "2026-06-10"},
        {"title": "合肥城市生命线：日均处理数据超百亿条", "url": "https://lw.news.cn/20260610/2e88b292332942c99bb7f880c69b9f50/c.html", "source": "瞭望", "date": "2026-06-10"},
        {"title": "安徽整省推进城市生命线安全工程合肥模式", "url": "https://lw.news.cn/20260610/2e88b292332942c99bb7f880c69b9f50/c.html", "source": "瞭望", "date": "2026-06-10"},
        {"title": "安徽芜湖城市生命线：累计监测预警各类险情281起", "url": "https://lw.news.cn/20260610/2e88b292332942c99bb7f880c69b9f50/c.html", "source": "瞭望", "date": "2026-06-10"},
        {"title": "规划十五五期间存量应急避难场所改造5万个", "url": "http://www.sdyanbao.com/detail/972524", "source": "中银证券", "date": "2026-06-05"},
        {"title": "规划十五五期间地下管网改造36.5万公里", "url": "http://www.sdyanbao.com/detail/972524", "source": "中银证券", "date": "2026-06-05"},
        {"title": "安全韧性从配套工作上升为城市更新刚性底线", "url": "http://www.chinajsb.cn/html/202606/04/57386.html", "source": "中国建设新闻网", "date": "2026-06-04"},
        {"title": "名列全球最安全城市之一，这座超大城市底气何来", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海应对台风巴威：459起高空排险，全市无人员伤亡", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海连续13年实现公众安全感、公安工作满意度双提升", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海徐汇老旧小区消防供水空管敷设工程", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海AI交通治堵智能体在1100余个路口部署", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海警方涉企风险预警模型覆盖企业全生命周期", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海率先探索划设外环内无人机飞行体验区", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海上半年举行1747场大型活动，万人以上718场", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "城市地下管网建设改造约77万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "燃气管网20万公里、排水管网17.5万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "供水管网17.5万公里、污水管网10万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "供热管网12万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "城市地下管网总长度约390万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "地下综合管廊累计建成约7700公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "城市生命线安全工程实现全流程闭环管理", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "应急避难场所改造5万个", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "房屋基础信息数字化率达95%以上", "url": "http://big5.www.gov.cn/gate/big5/www.gov.cn/zhengce/202605/content_7070588.htm", "source": "新华社", "date": "2026-05-29"},
        {"title": "上海公安睿鹰警用无人机处置交通事故3800多起", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海反诈中心实现被动止损向主动防骗转变", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "上海安全感不是零风险的承诺，而是从容应对风险的底气", "url": "http://chinapeace.gov.cn/chinapeace/c100045/2026-07/16/content_12847578.shtml", "source": "解放日报", "date": "2026-07-16"},
        {"title": "广州水务局与供电局签署战略合作协议，守护城市生命线", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "水电携手开启水电互保、协同共治政企合作新篇章", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "双方重点围绕规划建设协同、水电双向保障、防灾救灾联动四大领域合作", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "强化极端条件下水电互济互保能力，提升市民用水用电可靠性", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "健全联合响应和应急联动机制，降低灾害天气对城市运行影响", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "深化协同管护和抢修配合，共同守护地下生命线安全", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "推进水电深度协同，打破行业壁垒、推动水网与电网共建共享", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "打造水网与新型电网融合发展的标杆样板", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "广州筑牢城市安全韧性生命线，为高质量发展夯实物理底座", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "水电携手是落实中央六张网统筹建设部署的关键抓手", "url": "https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_10947463.html", "source": "广州市人民政府", "date": "2026-08-03"},
        {"title": "重点实施城镇供热温暖工程", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "十五五建设改造地下管网77万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "重庆沙坪坝区知天数字防汛系统，全链条提升城市韧性", "url": "https://baijiahao.baidu.com/s?id=1872735225133443122", "source": "新华社", "date": "2026-08-06"},
        {"title": "重庆数字防汛：AI+大数据实现全流域雨情水情汛情全面掌握", "url": "https://baijiahao.baidu.com/s?id=1872735225133443122", "source": "新华社", "date": "2026-08-06"},
        {"title": "城市地下管网是国家六张网之一，十五五建设改造约77万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "燃气管网20万公里、排水管网17.5万公里、供水管网17.5万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "污水管网10万公里、供热管网12万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "重点实施城镇供热温暖工程", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "统筹推进城市基础设施生命线安全工程建设", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "浙江宁波环城南路综合管廊根治马路拉链、空中蜘蛛网", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "安徽池州海绵城市建设达标率57.24%", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "《规划》明确十五五应急避难场所改造指标", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"}
    ],
    "四好建设": [
        {"title": "住建部：各地要系统推进好房子等四好建设", "url": "https://m.gmw.cn/2026-06/08/content_1304488080.htm", "source": "央视网", "date": "2026-06-08"},
        {"title": "住建部：十五五期间新开工改造城镇老旧小区11.5万个", "url": "https://politics.gmw.cn/2026-06/08/content_38817326.html", "source": "光明网", "date": "2026-06-08"},
        {"title": "住建部：未来五年系统推进四好建设", "url": "https://huacheng.gz-cmc.com/pages/2026/06/08/91d4f32a030845648d574f0a90e32b34.html", "source": "广州日报新花城", "date": "2026-06-08"},
        {"title": "推进城市更新 打造四好空间（经济新方位）", "url": "https://paper.people.com.cn/rmrb/pc/content/202608/03/content_30172706.html", "source": "人民日报", "date": "2026-08-03"},
        {"title": "视点 | 如何高质量推进城市更新？打造四好空间", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "中国城市规划学会", "date": "2026-08-03"},
        {"title": "推进城市更新 打造四好空间", "url": "https://www.163.com/dy/article/L3E52NQ405366JV6.html", "source": "中国城市规划协会", "date": "2026-08-03"},
        {"title": "聚焦民生工程，解读《城市更新十五五规划》", "url": "https://www.planning.org.cn/news/view?id=18767", "source": "中国建设报", "date": "2026-07-06"},
        {"title": "武汉市江汉区以五改四好焕活老街区", "url": "https://www.cnr.cn/hubei/jdt/20260804/t20260804_527745967.shtml", "source": "央广网", "date": "2026-08-04"},
        {"title": "上海闵行保障房项目：层高3米+双阳台，打造好房子", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "《四川省好住房评价标准》实施，全国首个地方标准", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "上海黄浦区市民新村：从老旧破到新绿美", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "北京华威北里：老旧小区引入物业服务，收缴率96%", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "天津中新生态城第四社区：5分钟生活圈", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "完整社区建设：2026年从试点转向扩面提质", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "十五五期间5000个社区实施完整社区建设改造", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "宁波环城南路综合管廊：根治马路拉链", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "安徽池州海绵城市达标率57.24%", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "十四五期间累计改造老旧小区24万多个", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "十四五期间加装电梯12.9万部", "url": "https://www.163.com/dy/article/L3EARROQ05346KFL.html", "source": "人民网", "date": "2026-08-03"},
        {"title": "住建部副部长秦海翔介绍《规划》四好建设部署", "url": "https://huacheng.gz-cmc.com/pages/2026/06/08/91d4f32a030845648d574f0a90e32b34.html", "source": "广州日报新花城", "date": "2026-06-08"},
        {"title": "建设好房子，改造老旧小区……城市更新聚焦23项重点任务", "url": "https://news.cctv.com/2026/06/09/ARTIVTA7IwtfkcedtBblRWbG260609.shtml", "source": "央视网", "date": "2026-06-09"},
        {"title": "城市更新聚焦23项重点任务（权威发布）", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "好房子特点：安全、舒适、绿色、智慧", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "实施房屋品质提升工程，突破一批关键技术", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "城镇老旧小区改造工程：新开工改造11.5万个", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "完整社区建设扩面提质增效：5000个社区建设改造", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "老旧街区厂区改造提升1500个", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "四好体系：好房子、好小区、好社区、好城区", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "完善社区养老、托育等公共服务设施", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "推进社区服务智能化", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "优化路网结构，提升通行效率", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "补齐停车设施短板", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "2026年是城市更新从试点探索走向系统落地关键年", "url": "http://beijing.creb.com.cn/rwtx/216585.jhtml", "source": "中国房地产报", "date": "2026-07-06"},
        {"title": "系统推进四好建设，解决群众身边关键小事", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "十四五累计改造老旧小区24万个，加装电梯12.9万部", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "增设停车位340多万个、养老托育设施6.4万个", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "打造口袋公园1.8万多个、城市绿道2.5万公里", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "国家历史文化名城145座、历史文化街区1300余片", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "历史建筑7.2万处，十五五修缮1.5万处", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "保护第一、应保尽保、以用促保", "url": "http://gd.people.com.cn/BIG5/n2/2026/0609/c123932-41604923.html", "source": "人民日报", "date": "2026-06-09"},
        {"title": "住建部：十五五新开工改造城镇老旧小区11.5万个", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "5000个社区实施完整社区建设改造", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "1500个老旧街区厂区实施改造提升", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "完善社区的养老、托育等公共服务设施", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "优化路网结构，提升通行效率，补齐停车设施短板", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "好房子建设作为民生工程重点推进", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "完整社区建设从试点转向扩面提质", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "城市更新从好房子、好小区、好社区、好城区四方面部署", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "建设好房子是城市更新的重要民生工程", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"},
        {"title": "老旧小区改造惠及群众切身利益", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "老旧小区改造提升公共空间和配套设施", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "老旧小区改造让居民生活更舒心", "url": "https://news.gmw.cn/2026-06/09/content_38818085.htm", "source": "光明日报", "date": "2026-06-09"},
        {"title": "推进城市更新 打造四好空间", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "好房子怎么建？从住有所居到住有宜居", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "从老旧破到新绿美：上海市民新村改造纪实", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "北京华威北里：老旧小区引入物业服务，收缴率96%", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "好社区是能承载生活温度的空间", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "天津中新生态城第四社区：5分钟生活圈", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "完整社区建设从试点转向扩面提质", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "十五五5000个社区实施完整社区建设改造", "url": "http://news.youth.cn/jsxw/202608/t20260803_16797159.htm", "source": "人民日报", "date": "2026-08-03"},
        {"title": "《城市更新十五五规划》对四好建设作出部署", "url": "http://jiwei.guiyang.gov.cn/xwhc/yw/202606/t20260615_90523470.html", "source": "光明日报", "date": "2026-06-08"},
        {"title": "广州越秀区十五五推进好房子、好小区、好社区、好城区建设", "url": "https://huacheng.gz-cmc.com/pages/2026/08/06/9a4249471b364f0dbe33a807ecd2a287.html", "source": "广州日报新花城", "date": "2026-08-06"}
    ],
    "城乡融合": [
        {"title": "透视109项重大工程⑤ | 如何推动城乡融合发展？", "url": "https://www.ndrc.gov.cn/wsdwhfz/202606/t20260601_1405603_ext.html", "source": "国家发改委", "date": "2026-06-01"},
        {"title": "融通城乡要素 激活融合新势能", "url": "http://m.chinadevelopment.com.cn/?s=index/article/id/1998502/url/http://www.chinadevelopment.com.cn/news/zj/2026/06/1998502.shtml", "source": "中国经济导报", "date": "2026-06-02"},
        {"title": "专家解读 | 段德罡：立足城乡融合，推进农业农村现代化", "url": "https://www.thepaper.cn/newsDetail_forward_33645708", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "专家解读 | 张秋玲：提升规划的战略导向作用", "url": "https://planning.org.cn", "source": "中国城市规划学会", "date": "2026-07-03"},
        {"title": "做好县域统筹 提升城乡要素配置增值效能", "url": "https://www.fujian.gov.cn/zwgk/ztzl/gjcjgxgg/px/202606/t20260609_7160813.htm", "source": "福建省人民政府", "date": "2026-06-09"},
        {"title": "鹰潭市打造全国城乡融合发展样板区2026年度工作要点", "url": "https://www.yingtan.gov.cn/art/2026/4/30/art_20485_1592617.html", "source": "鹰潭市人民政府", "date": "2026-04-30"},
        {"title": "人民日报整版聚焦：坚持协调发展，促进城乡融合和区域联动", "url": "https://www.peopleapp.com/column/30051172654-500007298381", "source": "人民日报", "date": "2026-01-09"},
        {"title": "从半城郊型经济感悟城乡融合（人民论坛）", "url": "http://paper.people.com.cn/rmrb/pc/content/202603/16/content_30145468.html", "source": "人民日报", "date": "2026-03-16"},
        {"title": "下好城乡一盘棋 奏响区域协奏曲", "url": "http://www.rmzxw.com.cn/c/2026-07-06/3941990.shtml", "source": "人民政协报", "date": "2026-07-06"},
        {"title": "破壁与共振：城乡融合发展驶入深水区", "url": "https://special.chinadevelopment.com.cn", "source": "中国经济导报", "date": "2026-03-12"},
        {"title": "以千万工程牵引城乡融合发展促共富", "url": "http://www.zjzx.gov.cn/zxyw/content_269579", "source": "浙江省政协", "date": "2026-08-04"},
        {"title": "宜宾城乡融合跑出振兴新范式", "url": "http://www.yibin.gov.cn/xxgk/jdhy/zcjd/mtjd/202607/t20260715_2242108.html", "source": "宜宾市人民政府", "date": "2026-07-15"},
        {"title": "广陵区：尴尬夹缝变身美丽转场", "url": "http://www.jiangsu.gov.cn/art/2026/8/3/art_33718_11811818.html", "source": "江苏省人民政府", "date": "2026-08-03"},
        {"title": "花都区深入实施百县千镇万村高质量发展工程", "url": "https://www.gz.gov.cn/xw/zwlb/gqdt/hdq/content/post_10947028.html", "source": "广州市人民政府", "date": "2026-07-31"},
        {"title": "城乡融合发展 要素顺畅流动", "url": "https://cpc.people.com.cn", "source": "人民网", "date": "2026-07-07"},
        {"title": "南海3+8镇村组团出道", "url": "https://www.sohu.com", "source": "搜狐", "date": "2026-08-03"},
        {"title": "全国政协常委尚勇：打好要素组合拳破解城乡融合难题", "url": "http://www.rmzxw.com.cn/c/2026-07-07/3943247.shtml", "source": "人民政协报", "date": "2026-07-07"},
        {"title": "专家解读 | 彭震伟：小城镇成为农民就近城镇化的温馨家园", "url": "https://www.thepaper.cn/newsDetail_forward_33661403", "source": "澎湃新闻", "date": "2026-07-26"},
        {"title": "全国政协常委王建军：城乡融合要把握合的内涵", "url": "http://www.rmzxw.com.cn/c/2026-07-06/3941990.shtml", "source": "人民政协报", "date": "2026-07-06"},
        {"title": "全国政协常委祝春秀：县域是城乡融合的结合点", "url": "http://www.rmzxw.com.cn/c/2026-07-06/3941990.shtml", "source": "人民政协报", "date": "2026-07-06"},
        {"title": "从乡土中国到城乡中国：乡村现代功能的重塑", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "十五五规划纲要：坚持城乡融合发展", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "2026年中央一号文件：坚持城乡融合发展", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "2025年末常住人口城镇化率达67.89%", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "从乡土中国到城乡中国：社会关系结构的转化", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村文化从符号保存走向功能重建", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村经济从单点开发走向城乡循环", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "以县域为重要支点完善城乡功能连接", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "把人的全面发展作为城乡融合的根本尺度", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村振兴既要塑形，也要铸魂", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村从被怀念的故乡转向可持续发展的现代空间", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡土文化以记忆、仪式、情感和媒介的方式存在", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村从土地中心的单一结构转向城乡联动的多元生计结构", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "人的身份呈现流动性、复合性和多重归属", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "城乡经济关系由二元结构转向相互嵌入的循环结构", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "县城和中心镇是连接城乡的重要节点", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村承担生产、生态、文化、治理和生活多重功能", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "城乡融合应使人可在城乡之间可进可退、可居可业", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "乡村文化只有重新进入人的生活，才能创造性转化", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "把乡村纳入城乡生活网络，形成收益可共享的城乡循环机制", "url": "http://www.ha.chinanews.com.cn/news/zx/2026/0804/70015.shtml", "source": "光明网", "date": "2026-08-04"},
        {"title": "珙县召开城乡融合发展试验区建设工作推进会", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "珙县县委书记强调坚持以规划为引领、以产业为先导、以适度聚居为方向", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "紧扣一核三中心四片空间发展布局，系统谋划镇域经济发展", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "推动一二三产融合发展，加大适度规模化经营主体培育", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "持续盘活闲置资源建设小微产业园，提高农产品附加值", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "扎实推进乡村聚居点建设，引导农村群众有序适度聚居", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "推动项目提质提速，谋划打基础、利长远的优质项目", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "推动产业连片提质，提升土地集约化利用水平", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "培育壮大新型经营主体，充实乡村产业人才队伍", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "延伸产业价值链，做大做强农产品流通体量", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "推动宜居和美乡村建设，改善乡村人居环境", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "升级完善基础设施配套，均衡优化公共服务供给", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "持续提升群众生活便利度，夯实基层治理、提升治理效能", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "构建县领导分片包联调度、部门指导、乡镇主责工作格局", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "优化资源分配，放大要素集聚叠加效应", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "集中资源打造一批标杆示范样板", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "健全差异化考核评价机制，常态化强化督导调度", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "巩固拓展脱贫攻坚成果，扎实推进乡村振兴", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "城乡融合试验区建设要注重示范成型", "url": "https://www.gongxian.gov.cn/ywdt/gxyw/202608/t20260803_2246249.html", "source": "珙县人民政府", "date": "2026-08-03"},
        {"title": "广州百千万工程从三年初见成效迈向五年显著变化", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州花都云山运动场项目：村集体资本参与公共设施BOT建设", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州从化鳌头镇西塘村90后村支书直播带货，打造西塘粉葛品牌", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州南沙大岗镇入选全省第一批小城市试点培育名单", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州环南昆山—罗浮山引领区400公里最美旅游公路贯通", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州海珠区宝业路消夜一条街连片整合，宝悦坊一期招商率达95%", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州涉农贷款余额4236亿元居全省首位", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州推进80项集成式改革，全域土地综合整治覆盖所有涉农区", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州从化流溪温泉广场驿站盘活闲置空间，节假日日均近8000人次", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "广州目标2030年实现34个建制镇镇村片区组团全覆盖", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"}
    ],
    "新质生产力": [
        {"title": "十五五规划里的新质生产力", "url": "https://www.ndrc.gov.cn/wsdwhfz/202604/t20260413_1404628.html", "source": "国家发改委", "date": "2026-04-13"},
        {"title": "把发展新质生产力摆在更加突出的战略位置", "url": "https://paper.people.com.cn/rmrb/pc/content/202603/12/content_30144875.html", "source": "人民日报", "date": "2026-03-12"},
        {"title": "发展新质生产力，为什么是必答题", "url": "https://gxt.hunan.gov.cn/gxt/xxgk_71033/gzdt/zhxw/202603/t20260305_33581897.html", "source": "湖南省工信厅", "date": "2026-03-05"},
        {"title": "习近平总书记为发展新质生产力作出新指引", "url": "https://www.gdcy.gov.cn", "source": "广东省产业园", "date": "2026-03-31"},
        {"title": "城市更新是一盘大棋 AI+催生新质生产力", "url": "https://tucsu.tsinghua.edu.cn/info/1042/2574.htm", "source": "中国经济时报", "date": "2026-06-02"},
        {"title": "张鸿辉：人工智能与一张图双向赋能，构建国土空间治理新质生产力", "url": "https://www.csgpc.org/detail/27625.html", "source": "中国城市规划学会", "date": "2026-06-26"},
        {"title": "培育壮大城市发展新动能", "url": "https://jxrb.jxwmw.cn/system/2026/08/02/031206821.shtml", "source": "江西日报", "date": "2026-08-02"},
        {"title": "蓝景丽家将变身国际交流中心，打造百年京张AI创新带", "url": "https://news.qq.com/rain/a/20260804A0447J00", "source": "北京日报", "date": "2026-08-03"},
        {"title": "武汉经开区：老厂区焕发年轻态，释放存量空间引入新质生产力", "url": "http://m.cnhubei.com/content/2026-07/17/content_20089831.html", "source": "湖北日报", "date": "2026-07-17"},
        {"title": "锚定新质生产力 20余省份差异化破局", "url": "https://www.hn.chinanews.com.cn", "source": "中新网", "date": "2026-01-06"},
        {"title": "各地频出新政加速培育新质生产力", "url": "https://finance.people.com.cn", "source": "人民网", "date": "2026-05-21"},
        {"title": "全域土地综合整治黄埔样本", "url": "https://www.hp.gov.cn", "source": "黄埔区政府", "date": "2026-07-03"},
        {"title": "智胜未来，新质动能更强劲（2026中国经济年中观察）", "url": "https://www.peopleapp.com/column/30052828977-500007630741", "source": "人民日报", "date": "2026-08-03"},
        {"title": "向新图强 蓄势未来——十五五开局之年中国产业发展观察", "url": "http://zqb.cyol.com/pc/content/202608/03/content_428925.html", "source": "新华社", "date": "2026-08-03"},
        {"title": "产业发展开新局｜十五五开局，产业转型看得见", "url": "https://news.cnr.cn", "source": "央广网", "date": "2026-08-03"},
        {"title": "看见中国经济新力量", "url": "https://paper.ce.cn", "source": "经济日报", "date": "2026-07-16"},
        {"title": "发展新质生产力 在实践中探索契合当地的创新范式", "url": "https://news.qq.com", "source": "新华网", "date": "2026-08-04"},
        {"title": "马向明：新动能培育关键在于认知成长逻辑变化", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "王世福：内涵提质本身就是存量中寻找高品质的价值增量", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "城市更新要服务于培育新质生产力和提升城市经济竞争力", "url": "https://tucsu.tsinghua.edu.cn/info/1042/2574.htm", "source": "清华大学", "date": "2026-06-02"},
        {"title": "长鑫发展，给中国城市创新转型打了样", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "践行人民城市理念，将创新驱动置于首位", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "北京大钟寺片区：传统商业空间转向数字经济复合功能", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "合肥围绕长鑫科技统筹推进能源保障和专业配套", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "上海张江科学城由产业园区向综合性科学城演进", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "创新产业依赖高效物流体系、公共服务和基础设施配套", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "科技创新需要科研、产业、人才与城市功能协同的生态支撑", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "合肥长期支持中科大，形成城校共生关系", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "合肥围绕集成电路产业链推动设计、材料、制造等协同发展", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "城市发展由粗放扩张转向内涵提质", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "坚持人民城市理念，把科技创新置于发展核心位置", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "以新质生产力加快塑造城市发展新动能", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "城市发展动能转换要求更注重科技创新和产业升级", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "创新位列现代化人民城市目标体系之首", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "集成电路等战略性新兴产业投资规模大、研发周期长", "url": "https://www.ctdsb.net/c1666_202608/2820685.html", "source": "极目新闻", "date": "2026-08-04"},
        {"title": "城市更新服务于培育新质生产力和提升城市经济竞争力（第二批）", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "推动老旧街区、老旧厂区转型升级，发展智能建造、低空经济", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "存量空间转化为流量入口", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新是价值投资而非财政负担", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新带动上下游技术创新", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "深圳福田发布新质产业社区，把新质产业装进社区", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田跳出传统路径，以空间重构牵引产业重塑", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "新质产业社区是没有围墙的创新综合体", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田提出对标曼哈顿+硅谷，坚持CBD+科创区发展战略", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田十百千行动计划锚定十大特色社区、百万产业空间、千亿资本活水", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田首批11个新质产业社区累计落地优质项目63个，总投资近50亿元", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "新质产业社区实现全域覆盖、轴带串联、片区适配、错位协同", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "深圳科创学院副院长于盈点赞产业社区理念", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田统筹250.82万平方米产业空间，政府国企社会物业齐发力", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田新增科技信贷超1096亿元，科创债发行量占全市一半", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "每个新质产业社区设立金融工作站，配备1银行+2创投金融顾问团", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田实施场景福地工程，半年新增171个场景机会", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "上步海洋经济社区专注蓝色经济赛道", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "梅林AI硬件创新产业社区完整搭建AI硬件全产业链生态", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "园岭智能制造产业社区深耕轻量化智能制造", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "东方富海陈玮：政府搭好骨架，让市场力量去发现、筛选、扶持", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "产业竞争正从单点技术突破转向创新生态体系整体较量", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "深圳福田发布新质产业社区，把新质产业装进社区", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田十百千行动计划：十大特色社区、百万产业空间、千亿资本活水", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "新质产业社区是没有围墙的创新综合体", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田首批11个新质产业社区累计落地项目63个，总投资近50亿元", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "梅林AI硬件创新产业社区完整搭建AI硬件全产业链生态", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田统筹250.82万平方米产业空间，政府国企社会物业齐发力", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "深圳科创学院副院长于盈点赞产业社区理念", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "每个新质产业社区设金融工作站，配备1银行+2创投金融顾问团", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "东方富海陈玮：政府搭好骨架，让市场力量去发现、筛选、扶持", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"},
        {"title": "福田初步形成上下楼即上下游、产业社区即产业生态发展格局", "url": "http://m2.people.cn/news/default.html?s=Ml8yXzQxNjI0MzEzXzIwMjg0Nl8xNzgyNzE2MjIx", "source": "人民网", "date": "2026-06-29"}
    ],
    "临时使用": [
        {"title": "自然资源部：加大存量土地盘活力度", "url": "https://xxzx.fj.gov.cn/jjxx/jjyj/202606/t20260608_7160528.html", "source": "人民网", "date": "2026-06-08"},
        {"title": "自然资源部住房城乡建设部发布新政支持城市更新行动", "url": "http://zrzy.jiangsu.gov.cn/nj/xwfj/gzdt/202601/t20260122_1926713.htm", "source": "自然资源部", "date": "2026-01-20"},
        {"title": "自然资源部：鼓励存量空闲地临时使用", "url": "http://zrgh.hd.gov.cn/xwdt/jnyw/202606/t20260610_2205252.html", "source": "国新办吹风会", "date": "2026-06-08"},
        {"title": "两部门推出六大措施支持城市更新行动", "url": "https://www2.xinhuanet.com", "source": "新华网", "date": "2026-01-21"},
        {"title": "自然资源部：把城市更新的红利落到老百姓家门口", "url": "http://finance.people.com.cn/n1/2026/0608/c1004-40736110.html", "source": "人民网", "date": "2026-06-08"},
        {"title": "衣霄翔：以临时使用激活存量更新新路径", "url": "https://www.planning.org.cn/law/view_news?id=18716", "source": "中国城市规划学会", "date": "2026-06-23"},
        {"title": "城市更新十五五规划大家谈系列解读", "url": "https://www.planning.org.cn", "source": "中国城市规划网", "date": "2026-06-23"},
        {"title": "自然资源部点赞广州：将街角闲置空地临时改造成公共绿地", "url": "https://huacheng.gz-cmc.com/pages/2026/06/08/7960101ae1924c559271a607d6f62fc0.html", "source": "广州日报", "date": "2026-06-08"},
        {"title": "山东青岛：闲置地块盘活利用，打造停车+休闲复合功能空间", "url": "http://dnr.shandong.gov.cn/xwdt_324/spxw/202606/t20260610_4971353.html", "source": "中国自然资源报", "date": "2026-06-10"},
        {"title": "武汉：出台储备土地临时利用管理办法，老纺织厂变音乐公园", "url": "https://3g.cjn.cn/Detail/?id=5523929&typeid=0", "source": "武汉晚报", "date": "2026-07-15"},
        {"title": "武汉：城市边角料变形记", "url": "https://whwb.cjn.cn/html/2026-06/04/content_152970_3500802.htm", "source": "武汉晚报", "date": "2026-06-04"},
        {"title": "湖南汨罗：闲置空地54天变身口袋公园", "url": "http://miluo-xhncloud.voc.com.cn/content/17294420", "source": "汨罗市融媒体中心", "date": "2026-07-06"},
        {"title": "广州：城市边角料变身金角银边", "url": "https://news.qq.com/rain/a/20260721A09ZP600", "source": "广州日报", "date": "2026-07-21"},
        {"title": "湖南怀化：出台已供未用土地临时利用管理办法", "url": "https://www.huaihua.gov.cn/huaihua/c100253/202608/26ebc860555744e88da57a6752ca269e.shtml", "source": "怀化市政府", "date": "2026-07-27"},
        {"title": "四川蓬安：创新探索储备土地临时盘活利用路径", "url": "https://dnr.sc.gov.cn", "source": "四川省自然资源厅", "date": "2026-07-16"},
        {"title": "老厂房老街区可按正面清单要求兼容科创、便民商业", "url": "http://zrgh.hd.gov.cn/xwdt/jnyw/202606/t20260610_2205252.html", "source": "国新办吹风会", "date": "2026-06-08"},
        {"title": "微更新项目可简化或豁免规划许可审批", "url": "http://zrgh.hd.gov.cn/xwdt/jnyw/202606/t20260610_2205252.html", "source": "国新办吹风会", "date": "2026-06-08"},
        {"title": "临时使用以先用起来替代等想好再用", "url": "https://www.planning.org.cn/law/view_news?id=18716", "source": "中国城市规划学会", "date": "2026-06-23"},
        {"title": "临时使用以低成本试错替代一次性决策", "url": "https://www.planning.org.cn/law/view_news?id=18716", "source": "中国城市规划学会", "date": "2026-06-23"},
        {"title": "存量时代规划和土地政策必须从刚性管控走向弹性适应", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "广州：深耕储备用地精细管理 盘活存量资源提质增效", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "广州创新打造边角地+新能源土地临时利用样板", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "黄埔茅岗路祺能2号、天河兴安路祺能8号综合充停车项目", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "融合快充、停车、洗车、公厕等便民功能", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "支持市政民生项目和受让企业办理临时借地", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "市本级临时用地约120万平方米，支持民生工程83万平方米", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "储备用地规范化围蔽整治，改善人居环境", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "机械大面积清除+人工精细化修整模式", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "严格落实净地出让标准，企业拿地即开工", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "探索三资盘活利用新机制", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "微更新项目可简化或豁免规划许可审批", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "存量时代规划和土地政策必须从刚性管控走向弹性适应（第二批）", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "规划和土地政策从管住走向激活", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "从单部门发力走向多部门协同", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "城市更新要适应市场不确定性，建立动态适应性管理政策", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "年度新增城乡建设用地原则上不超过盘活存量土地面积", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "通过硬约束倒逼地方政府将工作重心转向存量挖潜", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "复合利用推广、正面清单和豁免清单建立", "url": "https://m.thecover.cn/news_details.html?eid=PLj4V/YZcnyH90qSdq8Jkw==&timestamp=1785005090552", "source": "封面新闻", "date": "2026-07-06"},
        {"title": "储备用地多元化临时利用，挖掘存量土地价值", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "全链条管理构建土地高效利用新路径", "url": "https://nr.gd.gov.cn/xwdtnew/sxdt/content/post_4938266.html", "source": "广东省自然资源厅", "date": "2026-08-05"},
        {"title": "广州以一房一档数字化管理夯实公房盘活基础", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "广州推行以修代租、EPCO活化模式", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "文德园以修代租机制：修缮投入置换长期使用权", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "番禺先锋社区公开招标引入中建四局，打破价高者得传统", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "广州历史街区与公房活化运营促进中心搭建协同联动平台", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "公房统一归集是提升盘活效率的关键路径", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "广州闲置公房活化实现一栋活化带动一片更新", "url": "https://m.mp.oeeee.com/a/BAAFRD0000202608031637633.html", "source": "奥一网", "date": "2026-08-03"},
        {"title": "广州黄埔区：批出效率，临活用地", "url": "http://www.hp.gov.cn/gzjg/qzfgwhgzbm/qghhzrzyj/xwgg/content/post_10873510.html", "source": "广州市黄埔区政府", "date": "2026-06-26"},
        {"title": "黄埔区上半年累计审批临时利用土地18宗，面积约5万余平方米", "url": "http://www.hp.gov.cn/gzjg/qzfgwhgzbm/qghhzrzyj/xwgg/content/post_10873510.html", "source": "广州市黄埔区政府", "date": "2026-06-26"},
        {"title": "广州知识城恒运天然气热电联产项目临时用地助施工抢工期", "url": "http://www.hp.gov.cn/gzjg/qzfgwhgzbm/qghhzrzyj/xwgg/content/post_10873510.html", "source": "广州市黄埔区政府", "date": "2026-06-26"},
        {"title": "广州市视和医疗公司临时用地帮助快速完成开工准备", "url": "http://www.hp.gov.cn/gzjg/qzfgwhgzbm/qghhzrzyj/xwgg/content/post_10873510.html", "source": "广州市黄埔区政府", "date": "2026-06-26"},
        {"title": "让储备用地闲不住、项目建设慢不得", "url": "http://www.hp.gov.cn/gzjg/qzfgwhgzbm/qghhzrzyj/xwgg/content/post_10873510.html", "source": "广州市黄埔区政府", "date": "2026-06-26"},
        {"title": "黄埔区持续深化临时利用审批流程改革", "url": "http://www.hp.gov.cn/gzjg/qzfgwhgzbm/qghhzrzyj/xwgg/content/post_10873510.html", "source": "广州市黄埔区政府", "date": "2026-06-26"},
        {"title": "广州市百千万工程探索集体资金进入基础设施领域的可靠路径", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "花都云山运动场项目：村集体投资2亿元参与公共设施BOT建设", "url": "https://news.dayoo.com/guangzhou/202607/08/139995_54977313.html", "source": "大洋网", "date": "2026-07-08"},
        {"title": "《城市更新十五五规划》明确更大力度支持盘活存量土地", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "自然资源部在城市更新吹风会上介绍存量土地盘活政策", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"}
    ],
    "规划转型": [
        {"title": "聚焦城市更新时代的城市规划转型，中央城市工作会议召开一周年学术研讨会在京举行", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "城市更新时代呼唤城市规划转型", "url": "https://www.planning.org.cn/news/view?id=18823", "source": "中国城市规划网", "date": "2026-07-24"},
        {"title": "业内人士共话城市更新时代城市规划转型", "url": "https://m.cnfin.com/cy-lb//zixun/20260723/4445133_1.html", "source": "新华财经", "date": "2026-07-23"},
        {"title": "石楠：中国特色城市现代化——呼唤规划行业系统性重构", "url": "https://planning.org.cn/law/view_news?id=18363", "source": "中国城市规划学会", "date": "2026-03-16"},
        {"title": "2026全国城市规划学会工作会议 | 拥抱变革，守正创新", "url": "https://115.28.200.210", "source": "中国城市规划学会", "date": "2026-01-27"},
        {"title": "专家解读 | 黄卫东：存量时代城市更新的系统重构与多元共治", "url": "https://www.thepaper.cn/newsDetail_forward_33466956", "source": "澎湃新闻", "date": "2026-06-27"},
        {"title": "自然资源部徐小黎谈城市更新：刚性用地约束倒逼地方发展转向存量挖潜", "url": "https://m.thepaper.cn/newsDetail_forward_33523976", "source": "澎湃新闻", "date": "2026-07-06"},
        {"title": "规划要讲大局，把城市更新搞上去", "url": "https://m.thepaper.cn/newsDetail_forward_33532336", "source": "澎湃新闻", "date": "2026-07-07"},
        {"title": "广州落实《条例》实施的新要求，深化国土空间详细规划改革", "url": "https://ghzyj.gz.gov.cn/gkmlpt/content/10/10628/post_10628515.html", "source": "广州市规划和自然资源局", "date": "2026-01-05"},
        {"title": "推动规划工作更加适应城市更新行动需要", "url": "https://zjt.jiangxi.gov.cn", "source": "江西省住建厅", "date": "2026-01-26"},
        {"title": "低效用地的重生之路：黄埔以高水平规划赋能航天小镇落地", "url": "https://www.hp.gov.cn", "source": "广州市黄埔区政府", "date": "2026-06-13"},
        {"title": "规划70年：全球视野下的中国规划治理转型与创新", "url": "https://www.163.com", "source": "中国城市规划学会", "date": "2026-06-25"},
        {"title": "王富海：规划不是转型而是重构", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "王富海：从下象棋到下围棋", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "王世福：规划要从为增长规划转向为治理规划", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "石楠：规划要从静态蓝图转向动态全周期管控", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "石楠：城市规划核心价值转向存量空间提质、民生品质提升", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "马向明：存量规划重在帮助既有资产在不确定中重建连接", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "司马晓：呼吁另立城市更新法支撑存量时代精细化管理", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "吕斌：城市更新立法势在必行", "url": "https://www.thepaper.cn/newsDetail_forward_33643264", "source": "澎湃新闻", "date": "2026-07-23"},
        {"title": "新时期城市更新的核心导向（第二批）", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "范式转变：从增量扩张到存量提质", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "规划从依赖土地增量红利转向存量空间效益", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "规划导向从为增长服务转向为治理服务", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "规划从静态蓝图转向动态全周期管控", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "规划核心价值转向存量空间提质、民生品质提升（第二批）", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "存量规划重在帮助既有资产在不确定中重建连接（第二批）", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "规划不是转型而是重构（第二批）", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "从下象棋到下围棋的规划思维转变", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "呼吁另立城市更新法支撑存量时代精细化管理", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新立法势在必行（第二批）", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "规划体系需要整体性重构，而非局部修补", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新作为系统性重构健全中国特色城市规划体系", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "从房地产驱动转向产业、消费、民生、安全多轮协同", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新告别传统开发思维，学会算综合账、长远账", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "对地方政府、市场企业、市民提出新的能力要求", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新是复杂的系统工程而非工程技术问题", "url": "https://paper.people.com.cn/zgcsb/pc/content/202607/13/content_30168422.html", "source": "中国城市报", "date": "2026-07-13"},
        {"title": "城市更新成为国家战略，中央城市工作会议擘画蓝图", "url": "https://www.gov.cn/zccfh/2026nzccfh/20260608/wzsl/202606/content_7071439.htm", "source": "中国政府网", "date": "2026-06-08"},
        {"title": "城市更新工作从试点探索、粗放推进转向体系化、制度化", "url": "https://stcn.com/article/detail/4028015.html", "source": "每日经济新闻", "date": "2026-07-20"},
        {"title": "城市更新正式迈入规范化、精细化、全周期运营新阶段", "url": "https://stcn.com/article/detail/4028015.html", "source": "每日经济新闻", "date": "2026-07-20"},
        {"title": "中央城市工作会议召开一周年学术研讨会在京举行，聚焦城市更新时代的城市规划转型", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "马向明：存量规划重在帮助既有资产在不确定性中重建连接", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王富海：城市更新时代城市规划不是转型而是重构", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王富海：从下象棋到下围棋，规划体系需要根本性重构", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王世福：当前增量终结提法偏颇，内涵提质本身即在寻找价值增量", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王世福：详细规划编制与审批权应下放地方，激发地方活力", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "石楠：城市规划正从计划经济下的龙头地位转向治理平台", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "石楠：规划导向要从土地开发转向人居改善", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "石楠：规划方法从静态蓝图转向动态全周期管控", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "司马晓：建议国家另立专门法规支撑存量时代精细化管理", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "吕斌：城市更新涉及多元目标，传统规划面临三重转型", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "吕斌：呼吁深化制度设计，建立多元化城市更新参与机制", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "杨保军：存量时代城市更新以人为核心、以优化治理为主要手段", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "杨保军：规划改革应为重塑式改革，推行差异化双轨模式", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "郑德高：两个转向包含四个逻辑转变", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "郑德高：城市更新立法迫在眉睫", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "谭纵波：规划工作重心应从管制思维转向积极发展与提质增效", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王凯总结：改革应锚定两大方向——坚守人民城市理念、秉持改革创新思维", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "中央城市工作会议召开一周年学术研讨会在京举行", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王富海：城市更新时代城市规划不是转型而是重构", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王富海：从下象棋到下围棋，规划体系需要根本性重构", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "王世福：当前增量终结提法偏颇，内涵提质本身即在寻找价值增量", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "石楠：城市规划正从计划经济下的龙头地位转向治理平台", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "石楠：规划导向要从土地开发转向人居改善", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "石楠：规划方法从静态蓝图转向动态全周期管控", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "司马晓：建议国家另立专门法规支撑存量时代精细化管理", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "郑德高：两个转向包含四个逻辑转变", "url": "https://www.chinajsb.cn/html/202607/27/58641.html", "source": "中国建设新闻网", "date": "2026-07-27"},
        {"title": "城市发展两个转向：从快速增长期转向稳定发展期，从增量扩张转向存量提质", "url": "https://m.bjnews.com.cn/detail/1780895525129605.html", "source": "新京报", "date": "2026-06-08"}
    ],
    "智能建造": [],
    "数智孪生": []
}

# ===================== 合并静态与抓取数据 =====================
def merge_data(static_data, scraped_entries):
    merged = {kw: list(static_data.get(kw, [])) for kw in KEYWORDS}
    seen_titles = {kw: {item['title'] for item in merged[kw]} for kw in merged}
    for entry in scraped_entries:
        for kw in entry['keywords']:
            if kw in merged:
                if entry['title'] not in seen_titles[kw]:
                    merged[kw].append({
                        'title': entry['title'],
                        'url': entry['url'],
                        'source': entry['source'],
                        'date': entry['date']
                    })
                    seen_titles[kw].add(entry['title'])
    return merged

# ===================== 生成 HTML =====================
def generate_html(merged_data):
    icon_map = {
        "存量提质增效": "♻️",
        "城市更新十五五规划": "📜",
        "人本更新": "👤",
        "城市体检": "🩺",
        "安全韧性": "🛡️",
        "四好建设": "🏡",
        "城乡融合": "🌾",
        "新质生产力": "⚙️",
        "临时使用": "🔄",
        "规划转型": "🧭",
        "智能建造": "🤖",
        "数智孪生": "🔄"
    }
    tag_map = {
        "存量提质增效": "核心范式",
        "城市更新十五五规划": "纲领文件",
        "人本更新": "民生导向",
        "城市体检": "前置机制",
        "安全韧性": "底线思维",
        "四好建设": "四好体系",
        "城乡融合": "共同富裕",
        "新质生产力": "产业升级",
        "临时使用": "创新路径",
        "规划转型": "行业变革",
        "智能建造": "技术赋能",
        "数智孪生": "数字孪生"
    }
    js_data = []
    for kw in KEYWORDS:
        items = merged_data.get(kw, [])
        display_name = KEYWORD_ALIAS.get(kw, kw)
        js_data.append({
            'keyword': display_name,
            'icon': icon_map.get(kw, '📌'),
            'tag': tag_map.get(kw, ''),
            'items': items
        })

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
        .banner .banner-left { display: flex; align-items: center; gap: 1.2rem; flex: 1 1 auto; }
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
        .search-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            background: #fff;
            padding: 0.8rem 1.5rem;
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
            min-width: 150px;
        }
        .search-bar input[type="text"]:focus { border-color: #1d7a8c; }
        .search-bar select {
            padding: 0.6rem 1.2rem;
            border: 1px solid #d0ddee;
            border-radius: 40px;
            font-size: 1rem;
            background: #fff;
            outline: none;
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
        }
        .search-bar .clear-btn:hover { background: #d0ddee; }
        @media (max-width: 600px) {
            .search-bar { border-radius: 20px; padding: 1rem; flex-direction: column; }
            .search-bar input[type="text"], .search-bar select { width: 100%; }
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
        .news-list .meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #7a8c9e; margin-top: 0.2rem; }
        .news-list .meta .source { background: #f0f4fa; padding: 0.05rem 0.6rem; border-radius: 12px; color: #3d5a73; }
        .news-list .meta .date { color: #8a9bab; }
        .card-footer { margin-top: 0.8rem; padding-top: 0.6rem; border-top: 1px solid #ecf1f7; font-size: 0.75rem; color: #8a9bab; text-align: right; flex-shrink: 0; }
        .footer { margin-top: 3.5rem; text-align: center; font-size: 0.9rem; color: #6b7e93; border-top: 1px solid #dce5ef; padding-top: 1.8rem; }
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

    html_lines = []
    html_lines.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_lines.append(f'<title>{SITE_TITLE}</title>')
    html_lines.append(css)
    html_lines.append('</head><body>')
    html_lines.append('<div class="container">')

    html_lines.append('''
    <div class="banner" id="banner">
        <div class="banner-left">
            <span class="banner-icon" id="bannerIcon">🏙️</span>
            <div class="banner-text">
                <span class="banner-label">🔍 当前热点关键词</span>
                <span class="banner-keyword" id="bannerKeyword">存量提质增效</span>
            </div>
            <span class="banner-tag" id="bannerTag">核心范式</span>
        </div>
        <div class="banner-indicators" id="indicators"></div>
    </div>
    ''')

    total_entries = sum(len(v) for v in merged_data.values())
    html_lines.append(f'''
    <div class="header">
        <h1>🏙️ {SITE_TITLE}</h1>
        <p>基于 2026 年政策文件与行业动态，聚合十二大关键词下的最新新闻资讯</p>
        <span class="badge">📅 {datetime.datetime.now().strftime("%Y年%m月%d日")} · 共 {total_entries} 条</span>
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

    html_lines.append('<div class="grid" id="newsGrid"></div>')

    html_lines.append(f'''
    <div class="footer">
        <p>🤖 机器人每周一自动更新 · 数据来源于 RSS 聚合 · 仅供学习参考</p>
        <span style="font-size:0.8rem;">更新于 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
    </div>
    ''')

    html_lines.append('</div>')
    html_lines.append('<button class="back-to-top" id="backToTopBtn" aria-label="回到顶部">↑</button>')

    import json
    js_data_json = json.dumps(js_data, ensure_ascii=False)

    html_lines.append(f'''
    <script>
        const newsData = {js_data_json};
        const grid = document.getElementById('newsGrid');

        function renderCards(data) {{
            let html = '';
            data.forEach((group) => {{
                const itemsHtml = group.items.map(item => `
                    <li>
                        <a href="${{item.url}}" target="_blank">${{item.title}}</a>
                        <div class="meta">
                            <span class="source">${{item.source}}</span>
                            <span class="date">${{item.date}}</span>
                        </div>
                    </li>
                `).join('');
                html += `
                    <div class="card">
                        <div class="category">
                            <span class="icon">${{group.icon}}</span>
                            <h2>${{group.keyword}}</h2>
                            <span class="tag">${{group.tag || ''}}</span>
                        </div>
                        <ul class="news-list">${{itemsHtml}}</ul>
                        <div class="card-footer">📰 共 ${{group.items.length}} 条新闻</div>
                    </div>
                `;
            }});
            grid.innerHTML = html;
        }}
        renderCards(newsData);

        const searchInput = document.getElementById('searchInput');
        const regionFilter = document.getElementById('regionFilter');
        const clearBtn = document.getElementById('clearBtn');
        searchInput.addEventListener('input', function() {{
            const keyword = this.value.trim().toLowerCase();
            const filteredData = newsData.map(group => {{
                let filteredItems = group.items.filter(item =>
                    item.title.toLowerCase().includes(keyword)
                );
                return {{ ...group, items: filteredItems }};
            }}).filter(group => group.items.length > 0);
            renderCards(filteredData);
        }});
        clearBtn.addEventListener('click', function() {{
            searchInput.value = '';
            regionFilter.value = '';
            renderCards(newsData);
        }});

        const bannerIcon = document.getElementById('bannerIcon');
        const bannerKeyword = document.getElementById('bannerKeyword');
        const bannerTag = document.getElementById('bannerTag');
        const indicatorsContainer = document.getElementById('indicators');
        const keywords = newsData.map(g => ({{ name: g.keyword, icon: g.icon, tag: g.tag || '' }}));
        let currentIndex = 0, intervalId = null;
        function renderIndicators() {{
            indicatorsContainer.innerHTML = '';
            keywords.forEach((_, idx) => {{
                const dot = document.createElement('span');
                dot.className = 'dot' + (idx === currentIndex ? ' active' : '');
                dot.dataset.index = idx;
                dot.addEventListener('click', function() {{
                    goTo(parseInt(this.dataset.index, 10));
                }});
                indicatorsContainer.appendChild(dot);
            }});
        }}
        function updateBanner(index) {{
            const item = keywords[index];
            bannerIcon.textContent = item.icon;
            bannerKeyword.textContent = item.name;
            bannerTag.textContent = item.tag;
            const dots = indicatorsContainer.querySelectorAll('.dot');
            dots.forEach((dot, i) => {{
                dot.classList.toggle('active', i === index);
            }});
        }}
        function goTo(index) {{
            if (index < 0) index = keywords.length - 1;
            if (index >= keywords.length) index = 0;
            currentIndex = index;
            updateBanner(currentIndex);
            resetInterval();
        }}
        function next() {{ goTo(currentIndex + 1); }}
        function resetInterval() {{
            if (intervalId) clearInterval(intervalId);
            intervalId = setInterval(next, 4000);
        }}
        renderIndicators();
        updateBanner(0);
        resetInterval();
        const banner = document.getElementById('banner');
        banner.addEventListener('mouseenter', function() {{ if (intervalId) {{ clearInterval(intervalId); intervalId = null; }} }});
        banner.addEventListener('mouseleave', function() {{ if (!intervalId) intervalId = setInterval(next, 4000); }});

        const backBtn = document.getElementById('backToTopBtn');
        window.addEventListener('scroll', function() {{
            if (window.scrollY > 300) backBtn.classList.add('visible');
            else backBtn.classList.remove('visible');
        }});
        backBtn.addEventListener('click', function() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});
    </script>
    </body></html>
    ''')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    print("网页生成成功！")

if __name__ == "__main__":
    print("开始抓取新闻...")
    scraped = fetch_news()
    print(f"抓取到 {len(scraped)} 条新新闻")
    merged = merge_data(STATIC_DATA, scraped)
    total = sum(len(v) for v in merged.values())
    print(f"合并后共有 {total} 条新闻")
    generate_html(merged)
    print("全部搞定！")
