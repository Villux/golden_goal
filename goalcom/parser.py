def get_match_links_for_league(bs, league_id):
    table = bs.findAll('div', {'data-competition-id': league_id})[0]
    match_row_list = table.findAll('div', {'class': 'match-row-list'})[0]
    match_rows = match_row_list.findAll('div', {'class': 'match-row'})

    match_links = []
    for match_row in match_rows:
        match_main_data = match_row.findAll('div', {'class': 'match-main-data'})[0]
        match_links.append(match_main_data.a["href"])
    return match_links

def get_players(lineup):
    lineup_type = lineup.h2.get_text()
    data_list = []
    if lineup_type != "Manager":
        player_elems = lineup.ul.findAll("li")
        for player in player_elems:
            data_list.append(
                {
                    "url_id": player.a["href"],
                    "name": player.findAll('span', {'class': 'widget-match-lineups__name'})[0].get_text(),
                    "lineup_type": lineup_type.replace(" ", "").lower()
                }
            )
    return data_list

def get_team_name_from_lineup(lineup, home=True):
    team_label = "home" if home else "away"
    container = lineup.findAll("a", {"class": f"widget-match-header__team widget-match-header__team--{team_label}"})[0]
    return container.findAll("span", {"class": "widget-match-header__name--full"})[0].get_text()

def get_lineup(bs):
    team_a = bs.findAll('div', {'class': "widget-match-lineups__team-a"})
    team_b = bs.findAll('div', {'class': "widget-match-lineups__team widget-match-lineups__team-b widget-match-lineups__team--hidden"})

    data = {}
    data["home_team"] = get_team_name_from_lineup(bs, home=True)
    data["home_team_players"] = get_players(team_a[0])
    data["home_team_substitutes"] = get_players(team_a[1])

    data["away_team"] = get_team_name_from_lineup(bs, home=False)
    data["away_team_players"] = get_players(team_b[0])
    data["away_team_substitutes"] = get_players(team_b[1])
    return data
