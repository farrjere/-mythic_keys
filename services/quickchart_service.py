from quickchart import QuickChart, QuickChartFunction

class QuickChartService:
    def __init__(self):
        pass

    def create_player_dicts(self, players, week):
        player_dicts = []
        for player in players:
            if week == "tyrranical":
                player_dicts.append({'label': player.name,  'data': list(player.tyrrannical_keys.values())})
            else:
                player_dicts.append({'label': player.name,  'data': list(player.fort_keys.values())})
        return player_dicts

    def rating_bars(self, players: list, week):
        key_dicts = self.create_player_dicts(players, week)
        labels = list(players[0].fort_keys.keys())
        qc = QuickChart()
        qc.width = 750
        qc.height = 300
        qc.device_pixel_ratio = 2.0
        qc.background_color = "#313131"
        config = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": key_dicts
            }
        }
        qc.config = config
        return qc.get_url()

