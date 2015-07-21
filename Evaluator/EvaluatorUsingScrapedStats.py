__author__ = 'Kevin'

# anchor extraction from html document
from lxml import html
import requests
import Evaluator
#import sys
#sys.path.insert(0, 'C:/work/MMB/Player')
#import Player
from Player.Player import Player

class EvaluatorUsingScrapedStats(Evaluator.Evaluator):

    def __init__(self, cutoff):
        self.cutoff = cutoff

    @staticmethod
    def getBatterUrl(player):
        # sample url -- http://www.baseball-reference.com/players/gl.cgi?id=poseybu01&t=b&year=2015
        return 'http://www.baseball-reference.com/players/gl.cgi?id=' + player.getLastName().lower()[:5] + player.getFirstName().lower()[:2] +'01&t=b&year=2015'

    def getPlayerValue(self, player):
        score = 0
        if(player.getPosition() == 'p'):
            score += EvaluatorUsingScrapedStats.getPitcherScore(self.cutoff)
            #TODO::if the pitcher will be batting add their batter score
        else:
            score += EvaluatorUsingScrapedStats.getBatterScore(self.cutoff)

        return score

    @staticmethod
    def getBatterScore(cutoff):
        page = requests.get(EvaluatorUsingScrapedStats.getBatterUrl(player))
        tree = html.fromstring(page.text)
        stuff = tree.xpath('//tr[contains(@id,"batting_gamelogs")]')
        currentScore = 0
        iteration=0
        for i in reversed(stuff):
            hits = int(i.findtext('.//td[13]'))
            twoB = int(i.findtext('.//td[14]'))
            threeB = int(i.findtext('.//td[15]'))
            hr = int(i.findtext('.//td[16]'))
            rbi = int(i.findtext('.//td[17]'))
            runs = int(i.findtext('.//td[12]'))
            bb = int(i.findtext('.//td[18]'))
            sb = int(i.findtext('.//td[26]'))
            hbp = int(i.findtext('.//td[21]'))
            atBats = int(i.findtext('.//td[11]'))
            outs = atBats - hits
            scoreThatGame = hits + 2*twoB + 3*threeB + 4*hr + rbi + runs + bb + 2*sb + hbp - outs/float(4)
            print 'hits: ', hits, ', 2b: ', twoB, ', 3b: ', threeB, ', hrs: ', hr, ', rbi: ', rbi, ', runs: ', runs, ', bb: ', bb, ', sb: ', sb, ', hbp ', hbp, ', outs ', outs, ', score: ', scoreThatGame
            currentScore += scoreThatGame
            iteration += 1
            if(iteration >= cutoff):
                break
        return currentScore

    @staticmethod
    def getPitcherScore(cutoff):
        #TODO
        return 0

    def get_pitcher_batter_matchup(self, pitcher, batter):
        pitcher_batter_url = "http://www.baseball-reference.com/play-index/batter_vs_pitcher.cgi?batter=" \
                             + self.get_player_id(pitcher) + "&pitcher=" + self.get_player_id(batter)

    def get_player_id(self, player):
        last_name_substr = player.getLastName()[:5]
        first_name_substr = player.getFirstName()[:2]
        name_iteration_number = "01"

        return last_name_substr + first_name_substr + name_iteration_number

    def get_player_page_url(self, player):
        player_id_url = "http://www.baseball-reference.com/players/j/" + self.get_player_id(player) + ".shtml"

    def get_team(self, player):
        self.get_player_page_url(player)
        player_page = requests.get(EvaluatorUsingScrapedStats.getUrlToPull(self.get_player_page_url(player)))
        tree = html.fromstring(player_page.text)
        organization = tree.xpath("//span[contains(@itemprop, 'organization'])")
        print organization

        teams_years_split = organization.split(" ", 1)
        teams = teams_years_split[0]
        years = teams_years_split[1]

        last_team = teams.split("/")[-1]
        last_year = years.split("-")[-1]

        #if(last_year == "2015" and last_team ==


e = EvaluatorUsingScrapedStats(5)
#Player(name, position, team_number, fan_duel_id, fan_duel_cost, fan_duel_fppg)
player = Player.Player('Buster Posey', 'b', '1', '1', '1000', '3.2538')
score = e.getPlayerValue(player)
print 'Final score: ', score