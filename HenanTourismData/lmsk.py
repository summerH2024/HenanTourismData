import requests
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm

# 基础配置
BASE_URL = "https://you.ctrip.com/sight/luoyang198/8865.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "Referer": "https://you.ctrip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def get_comment_page(page_num, base_url, headers):
    """
    获取指定页码的评论数据（仅评分、评价标签、评论原文）
    返回：(当前页评论数据, 当前页完整爬取URL)
    """
    # 构造分页参数，适配携程评论分页逻辑
    params = {
        "scene": "online",
        "page": page_num,
        "orderBy": "default"
    }
    # 构造当前页完整URL（用于控制台打印）
    current_page_url = f"{base_url}?scene=online&page={page_num}&orderBy=default"
    
    try:
        # 发送GET请求，设置超时时间
        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # 抛出请求错误异常
        soup = BeautifulSoup(response.text, "html.parser")
        
        page_comments = []
        # 遍历所有评论项
        for item in soup.select(".commentItem"):
            # 1. 提取评分（1-5分）
            score = "未知"
            score_elem = item.select_one(".averageScore .scoreIcon")
            if score_elem and "src" in score_elem.attrs:
                if "score-5" in score_elem["src"]:
                    score = "5分"
                elif "score-4" in score_elem["src"]:
                    score = "4分"
                elif "score-3" in score_elem["src"]:
                    score = "3分"
                elif "score-2" in score_elem["src"]:
                    score = "2分"
                elif "score-1" in score_elem["src"]:
                    score = "1分"
            
            # 2. 提取评价标签（如超棒、不错）
            awesome_tag = item.select_one(".averageScore")
            tag = awesome_tag.get_text(strip=True).replace(score, "").strip() if awesome_tag else "无标签"
            
            # 3. 提取评论原文
            content_elem = item.select_one(".commentDetail")
            comment_content = content_elem.get_text(strip=True) if content_elem else "无评论内容"
            
            # 封装当前评论数据（适配CSV行数据格式）
            comment_info = [
                page_num,       # 页码
                score,          # 评分
                tag,            # 评价标签
                comment_content # 评论原文
            ]
            page_comments.append(comment_info)
            
            # 控制台打印当前这条评论的内容
            print(f"\n---------- 第 {page_num} 页 - 评论内容 ----------")
            print(f"评分：{score}")
            print(f"评价标签：{tag}")
            print(f"评论原文：{comment_content}")
            print(f"----------------------------------------")
        
        return page_comments, current_page_url
    
    except Exception as e:
        print(f"第 {page_num} 页爬取失败，错误信息：{str(e)}")
        return [], current_page_url

def main():
    """
    主函数：批量爬取300页评论并保存为CSV文件（含精细化分页统计、控制台打印、耗时统计）
    """
    total_pages = 300  # 你指定的总页数
    output_file = "lmsk_comments.csv"  # 输出的CSV文件名
    total_comment_count = 0  # 初始化总数据条数计数器
    
    # 记录爬取开始时间
    start_time = time.time()
    
    # 1. 打开CSV文件，初始化写入器（设置newline=''防止空行，encoding='utf-8-sig'解决中文乱码）
    with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        # 定义CSV表头
        fieldnames = ["页码", "评分", "评价标签", "评论原文"]
        writer = csv.writer(csvfile)
        
        # 2. 写入表头
        writer.writerow(fieldnames)
        
        # 3. 逐页爬取并写入数据
        for page in tqdm(range(1, total_pages + 1), desc="整体爬取进度"):
            # 爬取当前页数据，获取当前页评论列表和完整URL
            current_page_comments, current_page_url = get_comment_page(page, BASE_URL, HEADERS)
            current_page_count = len(current_page_comments)  # 当前页有效数据条数
            
            # 批量写入当前页的所有评论数据
            if current_page_comments:
                writer.writerows(current_page_comments)
            
            # ========== 新增：精细化分页统计打印 ==========
            total_comment_count += current_page_count  # 累加至总条数
            print(f"第 {page} 页完成，有效数据：{current_page_count} 条，累计：{total_comment_count}")
            print(f"爬取第 {page+1 if page < total_pages else '已全部完成'} 页：{current_page_url if page < total_pages else '无后续页码'}")
            
            # 暂停1.5秒，降低请求频率，避免触发反爬
            time.sleep(1.5)
    
    # 计算并格式化总耗时
    end_time = time.time()
    total_elapsed_time = end_time - start_time
    minutes = int(total_elapsed_time // 60)
    seconds = int(total_elapsed_time % 60)
    
    # 输出最终爬取结果、数据条数与耗时
    print(f"爬取完成！数据已保存到：{output_file}")
    print(f"核心统计结果：")
    print(f"总爬取页码：{total_pages} 页")
    print(f"有效评论数据条数：{total_comment_count} 条")
    print(f"爬取总耗时：{minutes} 分 {seconds} 秒（精确耗时：{total_elapsed_time:.2f} 秒）")

if __name__ == "__main__":
    main()