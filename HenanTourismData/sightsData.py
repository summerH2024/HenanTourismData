import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re


class CtripStaticPageCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://you.ctrip.com/",
        }
        # 河南景点分页URL
        self.base_url = "https://you.ctrip.com/sight/henan100058/s0-p{}.html"
        self.all_sights = []
        self.total_pages = 300  # 可手动调整爬取页数
        self.csv_file = "ctrip_henan_sights.csv"

    def parse_sight_item(self, item_tag):
        """单个景点解析，提取圆点前的城市地点"""
        sight_info = {
            "景点名称": "",
            "景区评级": "",
            "标签列表": [],
            "热度值": "",
            "评分": "",
            "评价数量": "",
            "地点": ""  # 仅保留圆点·前面的城市名称
        }

        try:
            # 1. 景点名称（优先从a标签title或文本提取）
            name_tag = item_tag.find('a', href=re.compile(r'/sight/.*\.html'))
            if name_tag:
                sight_info["景点名称"] = name_tag.get_text(strip=True) or name_tag.get('title', '').strip()

            # 2. 景区评级（5A/4A等）
            level_tag = item_tag.find('span', class_=re.compile(r'(level-text|5A|4A)'))
            if level_tag:
                sight_info["景区评级"] = level_tag.get_text(strip=True)

            # 3. 标签列表（提取特色标签，排除预订相关内容）
            tag_container = item_tag.find('div', class_=re.compile(r'rankInfoModule_tag_list|tag-list|short-features'))
            if tag_container:
                tag_tags = tag_container.find_all('span', class_=re.compile(r'tag-text|tag|feature'))
                sight_info["标签列表"] = [t.get_text(strip=True) for t in tag_tags if t.get_text(strip=True) and len(t.get_text(strip=True)) > 1]
            else:
                all_tags = item_tag.find_all('span', class_=re.compile(r'tag'))
                sight_info["标签列表"] = [t.get_text(strip=True) for t in all_tags 
                                        if t.get_text(strip=True) and '订' not in t.get_text() and '退' not in t.get_text()]

            # 4. 热度值
            heat_tag = item_tag.find('span', class_=re.compile(r'heat-score-value|heat-score_value'))
            if heat_tag:
                sight_info["热度值"] = heat_tag.get_text(strip=True)
            else:
                heat_match = re.search(r'(\d+\.?\d*)', item_tag.get_text())
                if heat_match and 0 < float(heat_match.group(1)) <= 10:
                    sight_info["热度值"] = heat_match.group(1)

            # 5. 评分
            score_tag = item_tag.find('span', class_=re.compile(r'comment-score-value|comment-score_value'))
            if score_tag:
                sight_info["评分"] = score_tag.get_text(strip=True)

            # 6. 评价数量（含“条点评”或“万条”）
            comment_tags = item_tag.find_all('span', class_=re.compile(r'comment-text|comment-count'))
            for tag in comment_tags:
                text = tag.get_text(strip=True)
                if '条点评' in text or '万条' in text:
                    sight_info["评价数量"] = text
                    break
            if not sight_info["评价数量"]:
                comment_match = re.search(r'([\d\.]+万?条点评?)', item_tag.get_text())
                if comment_match:
                    sight_info["评价数量"] = comment_match.group(0)

            # 7. 提取地点（仅保留圆点·前面的内容）
            location_tag = item_tag.find('span', class_=re.compile(r'distanceView_desc-text|location|address'))
            if location_tag:
                full_location = location_tag.get_text(strip=True)
                # 按圆点·分割，取前面的部分（兼容全角·和半角.，优先全角）
                if '·' in full_location:
                    sight_info["地点"] = full_location.split('·')[0].strip()
                elif '.' in full_location:
                    sight_info["地点"] = full_location.split('.')[0].strip()
                else:
                    # 无圆点时保留完整提取结果（兜底）
                    sight_info["地点"] = full_location
            else:
                # 正则备用：提取类似“洛阳·XX”的格式，仅保留前面城市
                loc_match = re.search(r'([\u4e00-\u9fa5]+)·', item_tag.get_text())
                if loc_match:
                    sight_info["地点"] = loc_match.group(1).strip()

        except Exception as e:
            print(f"解析出错：{e}")

        return sight_info

    def crawl_page(self, page_num):
        """爬取单页景点数据"""
        url = self.base_url.format(page_num)
        print(f"爬取第 {page_num} 页：{url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=20, verify=False)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # 匹配多种可能的景点容器标签
            sight_items = soup.find_all(['div', 'li', 'article'], class_=re.compile(
                r'sightItem|listItem|sight-item|item|card|box__sight|poi-item|sightCard|sight-list-item'
            ))

            if not sight_items:
                print(f"第{page_num}页未找到景点容器，可能class变更或页面无数据")
                print("页面部分内容：", soup.get_text()[:300])
                return False

            page_sights = []
            for item in sight_items:
                info = self.parse_sight_item(item)
                if info["景点名称"]:
                    page_sights.append(info)
                    print(f"  提取成功：{info['景点名称']} | {info['景区评级']} | {info['地点']} | 热度:{info['热度值']} | 评分:{info['评分']} | 点评:{info['评价数量']} | 标签:{', '.join(info['标签列表'])}")

            self.all_sights.extend(page_sights)
            print(f"第{page_num}页完成，有效数据：{len(page_sights)} 条，累计：{len(self.all_sights)}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return False

    def save_to_csv(self):
        """将爬取数据保存到CSV文件"""
        if not self.all_sights:
            print("无数据可保存")
            return

        with open(self.csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # CSV表头（包含提取的城市地点）
            writer.writerow(["景点名称", "景区评级", "地点", "标签列表", "热度值", "评分", "评价数量"])
            for sight in self.all_sights:
                tags_str = ", ".join(sight["标签列表"])
                writer.writerow([
                    sight["景点名称"],
                    sight["景区评级"],
                    sight["地点"],
                    tags_str,
                    sight["热度值"],
                    sight["评分"],
                    sight["评价数量"]
                ])
        print(f"数据已保存到 {self.csv_file}，共 {len(self.all_sights)} 条")

    def run(self):
        """启动爬虫主流程"""
        print("开始爬取携程河南景点...")
        start_time = time.time()

        for page in range(1, self.total_pages + 1):
            success = self.crawl_page(page)
            # 随机延时，避免被反爬
            time.sleep(random.uniform(4, 8))

            # 每10页保存一次数据，防止意外丢失
            if page % 10 == 0 or page == self.total_pages:
                self.save_to_csv()

            # 连续5页失败则提前结束，避免无效爬取
            if page > 5 and not success:
                print("连续多页失败，提前结束爬取")
                break

        end_time = time.time()
        print(f"\n爬取结束！耗时：{(end_time - start_time)/60:.2f} 分钟")
        print(f"总共获取 {len(self.all_sights)} 条有效数据")
        # 最终再保存一次完整数据
        self.save_to_csv()


if __name__ == "__main__":
    import warnings
    # 忽略无关警告信息，让输出更整洁
    warnings.filterwarnings('ignore')

    # 实例化并运行爬虫
    crawler = CtripStaticPageCrawler()
    crawler.run()