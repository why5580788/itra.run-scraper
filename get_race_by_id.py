from itra_scraper import get_race

def main():
    # 使用一个已知的比赛ID，例如91783（RESTONICA TRAIL by UTMB® - Tavignanu Trail）
    race_id = "91783"
    
    try:
        race_info = get_race(id=race_id)
        
        if race_info is None:
            print("Received None from get_race function.")
            return
        
        print(f"Event Name: {race_info['event_name']}")
        print(f"Race Name: {race_info['race_name']}")
        print(f"Date: {race_info['date']}")
        print(f"Distance: {race_info['distance']} km")
        print(f"Elevation Gain: {race_info['elevation_gain']} m")
        print(f"Number of Participants: {race_info['number_of_participants']}")
        print(f"About the Race: {race_info['about_the_race']}")
        
        # 打印比赛结果
        if 'results' in race_info and len(race_info['results']) > 0:
            print("\nRace Results:")
            for result in race_info['results']:
                print(f"Place: {result['place']}, "
                      f"Runner: {result['name']}, "
                      f"Time: {result['time']}, "
                      f"Race Score: {result['race_score']}, "
                      f"Age: {result['age']}, "
                      f"Gender: {result['gender']}, "
                      f"Nationality: {result['nationality']}")
        else:
            print("No race results available.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()