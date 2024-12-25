import requests
import logging
import pandas as pd
from datetime import datetime

# 设置日志记录级别为DEBUG，以便看到详细的输出
logging.basicConfig(level=logging.DEBUG)

def fetch_race_results(runner_id, cookies=None):
    url = "https://itra.run/api/Race/GetRaceResultsData"
    
    # 添加必要的头部信息以模拟浏览器行为
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': f'https://itra.run/RunnerSpace/{runner_id}',  # 确保正确的 Referer 头部信息
    }
    
    params = {
        'runnerId': runner_id,
        'pageNumber': 1,
        'pageSize': 20,
    }

    session = requests.Session()
    
    if cookies:
        session.cookies.update(cookies)

    try:
        print(f"Fetching race results for runner with ID {runner_id}...")
        
        response = session.get(url, headers=headers, params=params)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'raceResults' in data and isinstance(data['raceResults'], list):
                filter_data = [
                    {
                        '赛事': item.get('name', 'N/A'),
                        '组别': item.get('distance', 'N/A'),
                        '爬升': item.get('elevationGain', 'N/A'),
                        '时间': item.get('time', 'N/A'),
                        '表现分': item.get('score', 'N/A'),
                        'ITRA积分': item.get('itraPoint', 'N/A'),
                        '总排名': item.get('ranking', 'N/A'),
                        '总排名总人数': item.get('runnerCount', 'N/A'),
                        '性别排名': item.get('genderRanking', 'N/A'),
                        '性别总人数': item.get('genderRunnerCount', 'N/A'),
                    }
                    for item in data['raceResults']
                ]
                
                return filter_data
            else:
                print("No race results available.")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print("Response Headers:", response.headers)
            print("Response Content:", response.text)

    except Exception as e:
        print(f"An error occurred: {e}")

def save_to_excel(data, runner_id):
    if not data:
        print("No data to save.")
        return
    
    # 将数据转换为 DataFrame
    df = pd.DataFrame(data)
    
    # 动态生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"itra_{runner_id}_{timestamp}.xlsx"
    
    # 保存为 Excel 文件
    df.to_excel(filename, index=False)
    print(f"Race results have been saved to {filename}")

def main():
    runner_id = "5832293"  # 使用您提供的跑者ID
    
    # 提供实际的 Cookie（如果需要）
    cookies = {
        # 'cookie_name': 'cookie_value',
        # 'another_cookie_name': 'another_cookie_value',
    }

    results = fetch_race_results(runner_id, cookies)
    
    if results:
        save_to_excel(results, runner_id)

if __name__ == "__main__":
    main()