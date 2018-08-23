import logging
from datetime import datetime
from urllib import parse

from sofifa.utils import get_integeres_from_text

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
    return player_rows[0:-1]

def int_or_none(value):
    if value.isdigit():
        return int(value)
    return None

def string_or_none(value):
    if value == "N/A":
        return None
    return str(value)

def get_general(cols):
    data = {}
    a_elems = cols[0].findChildren(["a"])
    data["nationality"] = string_or_none(a_elems[0]["title"])
    data["name"] = string_or_none(a_elems[1]["title"])
    data["position"] = string_or_none(','.join([elem.span.get_text() for elem in cols[0].div.div.findChildren(["a"])]))
    data["age"] = int_or_none(cols[1].div.get_text())
    data["overall_rating"] = int_or_none(get_divspan(cols[2]))
    data["potential"] = int_or_none(get_divspan(cols[3]))
    data["club"] = string_or_none(cols[4].div.a.get_text())
    return data

def get_basic(cols):
    data = {}
    data["fifa_id"] = int_or_none(cols[0].div.get_text())
    data["height"] = int_or_none(get_integeres_from_text(cols[1].div.get_text()))
    data["weight"] = int_or_none(get_integeres_from_text(cols[2].div.get_text()))
    data["foot"] = string_or_none(cols[3].div.get_text())
    data["growth"] = int_or_none(cols[4].div.get_text())
    data["joined"] = string_or_none(cols[5].div.get_text())
    data["loan_date_end"] = string_or_none(cols[6].div.get_text())
    data["value"] = string_or_none(cols[7].div.get_text())
    data["wage"] = string_or_none(cols[8].div.get_text())
    data["release_clause"] = string_or_none(cols[9].div.get_text())
    return data

def get_attacking(cols):
    data = {}
    data["total_attacking"] = int_or_none(cols[0].div.get_text())
    data["crossing"] = int_or_none(get_divspan(cols[1]))
    data["finishing"] = int_or_none(get_divspan(cols[2]))
    data["heading_accuracy"] = int_or_none(get_divspan(cols[3]))
    data["short_passing"] = int_or_none(get_divspan(cols[4]))
    data["volleys"] = int_or_none(get_divspan(cols[5]))
    return data

def get_skill(cols):
    data = {}
    data["total_skill"] = int_or_none(cols[0].div.get_text())
    data["dribbling"] = int_or_none(get_divspan(cols[1]))
    data["curve"] = int_or_none(get_divspan(cols[2]))
    data["fk_accuracy"] = int_or_none(get_divspan(cols[3]))
    data["long_passing"] = int_or_none(get_divspan(cols[4]))
    data["ball_control"] = int_or_none(get_divspan(cols[5]))
    return data

def get_movement(cols):
    data = {}
    data["total_movement"] = int_or_none(cols[0].div.get_text())
    data["acceleration"] = int_or_none(get_divspan(cols[1]))
    data["sprint_speed"] = int_or_none(get_divspan(cols[2]))
    data["agility"] = int_or_none(get_divspan(cols[3]))
    data["reactions"] = int_or_none(get_divspan(cols[4]))
    data["balance"] = int_or_none(get_divspan(cols[5]))
    return data

def get_power(cols):
    data = {}
    data["total_power"] = int_or_none(cols[0].div.get_text())
    data["shot_power"] = int_or_none(get_divspan(cols[1]))
    data["jumping"] = int_or_none(get_divspan(cols[2]))
    data["stamina"] = int_or_none(get_divspan(cols[3]))
    data["strength"] = int_or_none(get_divspan(cols[4]))
    data["long_shots"] = int_or_none(get_divspan(cols[5]))
    return data

def get_mentality(cols):
    data = {}
    data["total_mentality"] = int_or_none(cols[0].div.get_text())
    data["aggression"] = int_or_none(get_divspan(cols[1]))
    data["interceptions"] = int_or_none(get_divspan(cols[2]))
    data["positioning"] = int_or_none(get_divspan(cols[3]))
    data["vision"] = int_or_none(get_divspan(cols[4]))
    data["penalties"] = int_or_none(get_divspan(cols[5]))
    data["composure"] = int_or_none(get_divspan(cols[6]))
    return data

def get_defending(cols):
    data = {}
    data["total_defending"] = int_or_none(cols[0].div.get_text())
    data["marking"] = int_or_none(get_divspan(cols[1]))
    data["standing_tackle"] = int_or_none(get_divspan(cols[2]))
    data["sliding_tackle"] = int_or_none(get_divspan(cols[3]))
    return data

def get_goalkeeping(cols):
    data = {}
    data["total_goalkeeping"] = int_or_none(cols[0].div.get_text())
    data["gk_diving"] = int_or_none(get_divspan(cols[1]))
    data["gk_handling"] = int_or_none(get_divspan(cols[2]))
    data["gk_kicking"] = int_or_none(get_divspan(cols[3]))
    data["gk_positioning"] = int_or_none(get_divspan(cols[4]))
    data["gk_reflexes"] = int_or_none(get_divspan(cols[5]))
    return data

def get_special(cols):
    data = {}
    data["total"] = int_or_none(cols[0].div.get_text())
    data["week_foot"] = int_or_none(cols[1].div.get_text())
    data["skill_moves"] = int_or_none(cols[2].div.get_text())
    data["attacking_work_rate"] = string_or_none(cols[3].div.get_text())
    data["defensive_work_rate"] = string_or_none(cols[4].div.get_text())
    data["international_reputation"] = int_or_none(cols[5].div.get_text())
    data["PAC"] = int_or_none(get_divspan(cols[6]))
    data["SHO"] = int_or_none(get_divspan(cols[7]))
    data["PAS"] = int_or_none(get_divspan(cols[8]))
    data["DRI"] = int_or_none(get_divspan(cols[9]))
    data["DEF"] = int_or_none(get_divspan(cols[10]))
    data["PHY"] = int_or_none(get_divspan(cols[11]))
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
