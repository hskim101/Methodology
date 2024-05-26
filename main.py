import time
import argparse

import google_news_cron

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('mode', type=str, choices=['once','interval','cron'], default='once', help="Choose how you want to run the code")
    parser.add_argument('--country', type=str, required=False, default='en', choices=['en','ko'], help="Which country will you search for news?")
    # parser.add_argument('--keyword', type=str, required=False, default='all', help="Enter keywords to crawl")
    args = parser.parse_args()
    keywords = ['firenoodle', '불닭', '불닭챌린지', 'firenoodlechallenge', 'koreanspicynoodle', '불닭볶음면', '핵붉닭', 'nuclearfirenoodle', 'noodlechallenge']
    for keyword in keywords:
        try:
            gooleNewsCron = google_news_cron.GoogleNewsCron()
            gooleNewsCron.run('once', args.country, keyword)
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            gooleNewsCron.stop()

if __name__=="__main__":
    main()