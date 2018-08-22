import logging
from datetime import datetime
from urllib import parse

from utils import get_integeres_from_text

class DateNotUniqueException(Exception):
    pass

def get_data_update_query_strings(bs):
    logging.debug('Starting to parse data dates from bs')
    datapoint_rows = bs.findAll('div', {'class': 'filter-body'})[0]

    dates = {}
    for drow in datapoint_rows.findAll('div', {'class': 'column col-4'})[4:]:
        month = drow.div.div.div.get_text()
        for child in drow.findAll('div', {'class': 'card-body'})[0].findChildren(["a"]):
            query_string = parse.urlparse(child["href"]).query
            day = child.get_text()
            date = datetime.strptime(f"{month} {day}", '%b %Y %d')
            date_string = date.strftime("%Y-%m-%d")

            if date in dates:
                logging.warning('All dates were not unique!')
                raise DateNotUniqueException("Date exists already, not unique!")
            else:
                dates[date_string] = query_string

    return dates

def get_divspan(col):
    return col.div.span.get_text()

def get_player_rows(bs):
    table = bs.findAll('table', {'class': 'table table-hover persist-area'})[0]
    tbody = table.findAll('tbody')[0]
    player_rows = tbody.findChildren(["tr"])
    return player_rows

def get_general(cols):
    data = {}
    a_elems = cols[0].findChildren(["a"])
    data["nationality"] = a_elems[0]["title"]
    data["name"] = a_elems[1]["title"]
    data["position"] = [elem.span.get_text() for elem in cols[0].div.div.findChildren(["a"])]
    data["age"] = int(cols[1].div.get_text())
    data["overall_rating"] = int(get_divspan(cols[2]))
    data["potential"] = int(get_divspan(cols[3]))
    data["club"] = cols[4].div.a.get_text()
    return data

def get_basic(cols):
    data = {}
    data["fifa_id"] = int(cols[0].div.get_text())
    data["height"] = int(get_integeres_from_text(cols[1].div.get_text()))
    data["weight"] = int(get_integeres_from_text(cols[2].div.get_text()))
    data["foot"] = cols[3].div.get_text()
    data["growth"] = int(cols[4].div.get_text())
    data["joined"] = cols[5].div.get_text()
    data["loan_date_end"] = cols[6].div.get_text()
    data["value"] = cols[7].div.get_text()
    data["wage"] = cols[8].div.get_text()
    data["release_clause"] = cols[9].div.get_text()
    return data

def get_attacking(cols):
    data = {}
    data["total_attacking"] = int(cols[0].div.get_text())
    data["crossing"] = int(get_divspan(cols[1]))
    data["finishing"] = int(get_divspan(cols[2]))
    data["heading_accuracy"] = int(get_divspan(cols[3]))
    data["short_passing"] = int(get_divspan(cols[4]))
    data["volleys"] = int(get_divspan(cols[5]))
    return data

def get_skill(cols):
    data = {}
    data["total_skill"] = int(cols[0].div.get_text())
    data["dribbling"] = int(get_divspan(cols[1]))
    data["curve"] = int(get_divspan(cols[2]))
    data["fk_accuracy"] = int(get_divspan(cols[3]))
    data["long_passing"] = int(get_divspan(cols[4]))
    data["ball_control"] = int(get_divspan(cols[5]))
    return data

def get_movement(cols):
    data = {}
    data["total_movement"] = int(cols[0].div.get_text())
    data["acceleration"] = int(get_divspan(cols[1]))
    data["sprint_speed"] = int(get_divspan(cols[2]))
    data["agility"] = int(get_divspan(cols[3]))
    data["reactions"] = int(get_divspan(cols[4]))
    data["balance"] = int(get_divspan(cols[5]))
    return data

def get_power(cols):
    data = {}
    data["total_power"] = int(cols[0].div.get_text())
    data["shot_power"] = int(get_divspan(cols[1]))
    data["jumping"] = int(get_divspan(cols[2]))
    data["stamina"] = int(get_divspan(cols[3]))
    data["strength"] = int(get_divspan(cols[4]))
    data["long_shots"] = int(get_divspan(cols[5]))
    return data

def get_mentality(cols):
    data = {}
    data["total_mentality"] = int(cols[0].div.get_text())
    data["aggression"] = int(get_divspan(cols[1]))
    data["interceptions"] = int(get_divspan(cols[2]))
    data["positioning"] = int(get_divspan(cols[3]))
    data["vision"] = int(get_divspan(cols[4]))
    data["penalties"] = int(get_divspan(cols[5]))
    data["composure"] = int(get_divspan(cols[6]))
    return data

def get_defending(cols):
    data = {}
    data["total_defending"] = int(cols[0].div.get_text())
    data["marking"] = int(get_divspan(cols[1]))
    data["standing_tackle"] = int(get_divspan(cols[2]))
    data["sliding_tackle"] = int(get_divspan(cols[3]))
    return data

def get_goalkeeping(cols):
    data = {}
    data["total_goalkeeping"] = int(cols[0].div.get_text())
    data["gk_diving"] = int(get_divspan(cols[1]))
    data["gk_handling"] = int(get_divspan(cols[2]))
    data["gk_kicking"] = int(get_divspan(cols[3]))
    data["gk_positioning"] = int(get_divspan(cols[4]))
    data["gk_reflexes"] = int(get_divspan(cols[5]))
    return data

def get_special(cols):
    data = {}
    data["total"] = int(cols[0].div.get_text())
    data["week_foot"] = int(cols[1].div.get_text())
    data["skill_moves"] = int(cols[2].div.get_text())
    data["attacking_work_rate"] = cols[3].div.get_text()
    data["defensive_work_rate"] = cols[4].div.get_text()
    data["international_reputation"] = int(cols[5].div.get_text())
    data["PAC"] = int(get_divspan(cols[6]))
    data["SHO"] = int(get_divspan(cols[7]))
    data["PAS"] = int(get_divspan(cols[8]))
    data["DRI"] = int(get_divspan(cols[9]))
    data["DEF"] = int(get_divspan(cols[10]))
    data["PHY"] = int(get_divspan(cols[11]))
    return data

def get_player_data(player):
    columns = player.findChildren(["td"])

    general = get_general(columns[1:6])
    basic = get_basic(columns[6:16])
    attacking = get_attacking(columns[16:22])
    skill = get_skill(columns[22:28])
    movement = get_movement(columns[28:34])
    power = get_power(columns[34:40])
    mentality = get_mentality(columns[40:47])
    defending = get_defending(columns[47:51])
    goalkeeping = get_goalkeeping(columns[51:57])
    special = get_special(columns[57:69])

    return {**general, **basic, **attacking, **skill, **movement, **power, **mentality, **defending, **goalkeeping, **special}


def parse_player_data(bs):
    player_rows = get_player_rows(bs)
    return [get_player_data(player) for player in player_rows]
