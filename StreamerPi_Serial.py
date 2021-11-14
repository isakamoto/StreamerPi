import webscrape

class Application():
    def __init__(self, webscrape_obj):
        self.obj = webscrape_obj
        self.league_dic = self.obj.league_dic
    
    def show_league_matches(self):

        # Create a dictionary [league name]
        league_choice = []
        
        # Create a dictionary {league : [match_description] }
        match_description_choice = {}

        for league in self.league_dic:
            league_choice.append(league)
            match_description_choice[league] = []
            for match_description in self.league_dic[league]:
                match_description_choice[league].append(match_description)

        for i in range (len(league_choice)):
            print (f"{i+1}) {league_choice[i]}")
        print()
        choice = int(input("Enter Choice Number of League to View: ")) - 1
        print()


        for i in range(len(match_description_choice[league_choice[choice]])):
            print (f"{i+1}) {match_description_choice[league_choice[choice]][i]}")
        print()
        choice_match = int(input("Enter Choice Number of Match to View: ")) - 1
        print()

        self.curr_league = league_choice[choice]
        self.curr_match = match_description_choice[self.curr_league][choice_match]
        self.obj.get_matches_urls(self.curr_league, self.curr_match)
        self.curr_match_link = self.league_dic[self.curr_league][self.curr_match]['stream_link']

    def get_m3u8_links(self):
        test_link = "https://uhdstreams.club/chat/ch7.php"
        self.obj.init_selenium()
        print(self.obj.video_finder(test_link))

if __name__ == "__main__":
    obj = webscrape.WebScrape()
    application = Application(obj)
    
    #application.show_league_matches()
    application.get_m3u8_links()