import pandas as pd
from itra_scraper import get_runners

def export_to_excel(runners, filename="runners.xlsx"):
    field_descriptions = {
        "runnerId": "跑者ID",
        "rank": "排名",
        "pi": "表现指数 (PI)",
        "name": "姓名",
        "hide": "隐藏状态",
        "firstName": "名字",
        "lastName": "姓氏",
        "ageGroup": "年龄组",
        "age": "年龄",
        "profilePic": "个人照片链接",
        "nationality": "国籍",
        "countryCode": "国家代码图片链接",
        "gender": "性别"
    }

    # 将数据转换为 DataFrame 并重命名列
    df = pd.DataFrame(runners)
    df.rename(columns=field_descriptions, inplace=True)

    # 导出为 Excel 文件
    df.to_excel(filename, index=False)
    print(f"跑者信息已成功导出到 '{filename}' 文件中。")

def main():
    country_code = "CHN"
    
    try:
        print(f"从 {country_code} 获取跑者信息...")
        runners = get_runners(country_code=country_code, count=10)
        
        if not runners:
            print(f"未找到符合国家代码 '{country_code}' 的跑者。")
        else:
            export_to_excel(runners)

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()