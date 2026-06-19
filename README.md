# HenanTourismData 河南旅游景点爬虫项目
## 项目介绍
基于Python的河南各地市旅游景区、游客评论爬虫，抓取携程景点基础信息+用户真实评价，输出CSV结构化数据，可用于旅游数据分析、可视化、大数据入库。

## 目录说明
1. 各地市爬虫脚本：`xx.py`
   - hnbwg.py：鹤壁景点爬虫
   - kfbwg.py：开封景点爬虫
   - ljs.py：洛阳景点爬虫
   - lmsk.py：龙门石窟专项爬虫
   - lybwg.py：洛阳博物馆爬虫
   - qmshy.py：清明上河园爬虫
   - sdhclydjq.py、sdhlydjq：嵩山/少林寺相关爬虫
   - sls.py：嵩山专项爬虫
   - wsswxc.py：万仙山爬虫
   - xiecheng.py：携程通用爬取封装
   - zzhnxjhc.py：郑州景点爬虫
   - sightsData.py：数据整合、清洗工具脚本
2. 数据文件 `.csv`
   - `ctrip_henan_sights.csv`：河南全量景点基础信息
   - `*_comments.csv`：对应地市景区游客评论数据集
3. requirements.txt：项目全部Python依赖库清单
4. test.py：简易测试脚本

## 环境依赖
Python >=3.9
安装依赖命令：
```bash
pip install -r requirements.txt
