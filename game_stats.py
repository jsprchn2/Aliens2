import json


class GameStats():
    # track statistics for alien invasion

    def __init__(self, ai_settings):
        # initialize stats
        self.ai_settings = ai_settings

        self.ships_left = 0
        self.aliens_start = None
        self.next_speedup = None
        self.aliens_left = None
        self.high_score = None
        self.high_scores_all = None
        self.score = None
        self.level = None

        self.reset_stats()
        # state alien invasion in an inactive state
        self.game_active = False
        # high score don't reset
        # self.high_score = 0

        # self.show_hi_score = False

        self.initialize_high_score()

    def reset_stats(self):
        # initialize stats that can change
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def initialize_high_score(self):
        try:
            with open('hi_scores.json', 'r') as file:
                self.high_scores_all = json.load(file)  # Cast to int to verify type
                self.high_scores_all.sort(reverse=True)
                self.high_score = self.high_scores_all[0]
        except (FileNotFoundError, ValueError, EOFError, json.JSONDecodeError, AttributeError, IndexError) as e:
            print(e)
            self.high_scores_all = [0, 0, 0]    # Some issue with the file, going to default
            self.high_score = self.high_scores_all[0]

    def save_high_score(self):
        # save to json file
        for i in range(len(self.high_scores_all)):
            if self.score >= self.high_scores_all[i]:
                self.high_scores_all[i] = self.score
                break
        with open('hi_scores.json', 'w') as file:
            json.dump(self.high_scores_all, file)
