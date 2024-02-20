import streamlit as st
from utils.config import settings
from utils.riot import *
from utils.graph import *
import pandas as pd
import json


st.set_page_config(
    page_title="Porostream",
    page_icon="img/favicon.png",
    layout="wide")

# TODO: Sidebar
with st.sidebar:
    st.write("## 📝About the project")
    st.markdown(
        "Porostream lets you analyze your League of Legends history to give you a deeper understanding of your performance.")

# NOTE: SEARCH INPUT
with st.sidebar:
    st.header("🔍Search summoner")
    values = st.text_input(
        "Enter name and tag separated by comma", "Obiwan ,HYM").split(',')
    name, tag = [value.strip() for value in values]
    region = st.selectbox(
        'Choose your region',
        ('VN2', 'OC1'), index=None)
    if region == 'OC1':
        mode = st.selectbox(
            'Choose game mode',
            ('Ranked Solo', 'Normal Draft'), index=None)
    else:
        mode = st.selectbox(
            'Choose game mode',
            ('Ranked Solo', 'Ranked Flex', 'Normal Blind', 'Normal Draft'), index=None)

    run = st.button("Find out")

# TODO: Main
st.markdown("""<h1 style='
                font-family: Recoleta-Regular; font-weight: 400; color: #ffc300;
                font-size: 3.5rem'>How Bad Is Your League</h1>""",
            unsafe_allow_html=True)

st.markdown("""<h3 style='
                font-family: Recoleta-Regular; font-weight: 400; color: #F0E6D2;
                font-size: 1.55rem'>Our sophisticated A.I. judges your awful gameplay</h3>""",
            unsafe_allow_html=True)
"""
![Python](https://img.shields.io/badge/python%203.10-3670A0?style=for-the-badge&logo=python&logoColor=fafafa)
![Plotly](https://img.shields.io/badge/plotly%20-%2300416A.svg?&style=for-the-badge&logo=pandas&logoColor=white)
![Riot Games](https://img.shields.io/badge/riotgames-D32936.svg?style=for-the-badge&logo=riotgames&logoColor=white)
"""
st.image("img/poros.jpg")
st.write("##")
st.subheader("🔒Team info is locked")
password = st.text_input("Enter password to unlock team info", type="password")


if password == "HYM":
    # NOTE: TEAM RANKED
    st.write("##")
    with open('team.json', 'r') as f:
        team = json.load(f)

    l, r = st.columns([1, 2])
    with l:
        st.header("📑Team ranked")
    with r:
        selected_player = st.selectbox(
            'Summoner', list(team.keys()), index=4)

    data = team[selected_player]
    l, m, r = st.columns([1, 1, 1])

    with l:
        st.image(
            f"https://ddragon.leagueoflegends.com/cdn/13.23.1/img/profileicon/{data['icon']}.png", width=250)
        st.link_button("Summoner Profile",
                       f"https://www.op.gg/summoners/vn/{data['name']}")
    with m:
        queue = {'RANKED_SOLO_5x5': 'Soloqueue',
                 'RANKED_FLEX_SR': 'Ranked Flex'}
        st.write(
            f"""<span style='font-weight: 200; font-size: 1rem'>{data['tier']} {data['rank']} {queue[data['queue']]}</span>""", unsafe_allow_html=True)
        st.write(
            f"""<span style='font-family: Recoleta-Regular; font-weight: 400; font-size: 2.5rem'>{data['name']}</span>""", unsafe_allow_html=True)

        wins, losses = data['wins'], data['losses']
        st.subheader(f":blue[{wins}]W - :red[{losses}]L")
        st.write(f"`Level`: {data['level']}")
        st.write(f"`LP`: {data['lp']}")
        st.write(f"`Winrate`: {((wins/(wins+losses))*100):.1f}%")
    with r:
        st.image(f"img/rank/{data['tier'].upper()}.png", width=300)

    # NOTE: LEADERBOARD
    st.write("##")
    df = pd.read_csv("extract.csv")

    st.header("⭐Leaderboard")
    tab1, tab2 = st.tabs(
        ["Damage on Champions", "Vision Score"])

    with tab1:
        l, r = st.columns([1, 1.5])
        with l:
            data = df.groupby('summonerName')[
                'totalDamageDealtToChampions'].mean().to_dict()
            fig = graph_dmg(data)
            st.plotly_chart(fig, use_container_width=True)

        with r:
            tru = df.groupby('summonerName')[
                'trueDamageDealtToChampions'].mean().to_dict()
            phy = df.groupby('summonerName')[
                'physicalDamageDealtToChampions'].mean().to_dict()
            mag = df.groupby('summonerName')[
                'magicDamageDealtToChampions'].mean().to_dict()

            names = list(tru.keys())
            physicals = list(phy.values())
            trues = list(tru.values())
            magics = list(mag.values())
            fig = graph_dmgproportion(names, trues, physicals, magics)
            st.plotly_chart(fig, use_container_width=True)
    with tab2:
        l, r = st.columns([1, 1])
        with l:
            data = df.groupby('summonerName')['visionScore'].mean().to_dict()
            fig = graph_vision(data)
            st.plotly_chart(fig, use_container_width=True)
        with r:
            st.subheader("What's a good vision score?")
            st.write(
                "A good vision score is `1.5x` the game length, a great vision score is more in the `2x` ballpark.")
            st.write("That doesn't mean just spam wards everywhere because a high vision score does nothing if you don't have good vision on things that **MATTER**.")
            fig = graph_winrate(df)
            st.plotly_chart(fig, use_container_width=True)

if run:
    if region is None:
        raise MissingRegionError("Please choose your region")
    if mode is None:
        raise MissingQueueError("Please choose game mode")
    queues = {
        "Ranked Flex": 440,
        "Ranked Solo": 420,
        "Normal Blind": 430,
        "Normal Draft": 400,
        "ARAM": 450
    }
    TOKEN = settings.TOKEN
    try:
        puuid = get_puuid(TOKEN, name, tag)
        summoner = get_info(TOKEN, puuid, region)
        ranks = get_rank(TOKEN, summoner, region)
        ranks = ranks[0] if ranks else ranks
        queue_id = queues[mode]

        ids = get_match_ids(TOKEN, puuid, 20, queue_id)
    except KeyError:
        st.error("🍎Summoner not found")
    else:
        with st.spinner(f"⌛Extracting data for `{name}`"):
            match_df, player_df = gather_data(TOKEN, puuid, ids)
            stats = transform(match_df, player_df)
        # NOTE: PROFILE
        st.write("##")
        l, m, r = st.columns([1, 1, 1])
        with l:
            st.image(
                f"https://ddragon.leagueoflegends.com/cdn/13.23.1/img/profileicon/{summoner['profileIconId']}.png", width=250)
            st.link_button("Summoner Profile",
                           f"https://www.op.gg/summoners/{'vn' if region == 'VN2' else region}/{name}-{tag}")
        with m:
            queue = {
                'RANKED_SOLO_5x5': 'Soloqueue',
                'RANKED_FLEX_SR': 'Ranked Flex'
            }
            st.write(f"""<span style='
                    font-weight: 200; font-size: 1rem'>{ranks['tier'].capitalize()} {ranks['rank']} {queue[ranks['queueType']]}</span>""",
                     unsafe_allow_html=True)
            st.write(f"""<span style='
                    font-family: Recoleta-Regular; font-weight: 400;
                    font-size: 2.5rem'>{name}</span>""",
                     unsafe_allow_html=True)

            wins = ranks['wins']
            losses = ranks['losses']
            st.subheader(f":blue[{wins}]W - :red[{losses}]L")
            st.write(
                f"`Level`: {summoner['summonerLevel']} - :green[{ranks['leaguePoints']}]LP")
            st.write(f"`Winrate`: {((wins/(wins+losses))*100):.1f}%")
        with r:
            st.image(f"img/rank/{ranks['tier']}.png", width=300)

        # NOTE: STATS
        st.write("##")
        st.header("📌Last 10 games")
        tab1, tab2 = st.tabs(
            ["Summary", "Metrics over Time"])
        with tab1:
            l, m, r = st.columns([1, 1, 1])
            with l:
                st.subheader("🎯Games")
                st.subheader(
                    f"{stats['wins'] + stats['loses']}G {stats['wins']}W {stats['loses']}L")
            with m:
                st.subheader("🏆Winrates")
                st.subheader(f"{(stats['wins']/10)*100:.1f} %")
            with r:
                st.subheader("⚔️KDA")
                st.subheader(
                    f"{stats['kills']}/{stats['deaths']}/{stats['assists']}")

            l, m, r = st.columns([1, 1, 1])
            with l:
                st.subheader("🥊Damage")
                st.subheader(f"{stats['dmg']:,.0f}")
            with m:
                st.subheader("👑Pentakills")
                st.subheader(stats['penta'])
            with r:
                st.subheader("💡Vision")
                st.subheader(stats['vision'])

            l, m, r = st.columns([1, 1, 1])
            with l:
                st.subheader("⛏️CSperMin")
                st.subheader(stats['cspermin'])
            with m:
                st.subheader("🥷Objectives")
                st.subheader(f"Max {stats['objsStolen']} stolen")
            with r:
                st.subheader("☁️Time alive")
                st.subheader(f"Longest {int(stats['timealive'])} min")
        with tab2:
            fig = graph_personal(match_df, player_df)
            st.plotly_chart(fig, use_container_width=True)

            fig = graph_dmgpersonal(match_df, player_df)
            st.plotly_chart(fig, use_container_width=True)

            st.info("📘Follow the link below for more visualisations")
            st.link_button("League of Graphs",
                           f"https://www.leagueofgraphs.com/summoner/{'vn' if region == 'VN2' else 'oce'}/{name}-{tag}")

        # NOTE: STATS
        st.write("##")
        st.header("🏆Champions")
        stats = ['totalDamageDealtToChampions', 'kills', 'deaths', 'assists']

        # Create a DataFrame with the aggregated data
        agg_stats_df = player_df.groupby('championName')[stats].mean()
        agg_stats_df['kda'] = (
            agg_stats_df['kills'] + agg_stats_df['assists']) / agg_stats_df['deaths'].replace(0, 1)

        # Create another DataFrame for winrate
        agg_winrate_df = player_df.groupby('championName')[
            'win'].value_counts().unstack(fill_value=0)
        agg_winrate_df['winrate'] = (
            agg_winrate_df[True] / (agg_winrate_df[True]+agg_winrate_df[False]))*100

        # Include win and lose count columns
        agg_winrate_df = agg_winrate_df.reset_index().rename(
            columns={True: 'win', False: 'lose'})

        # Merge the two DataFrames on 'championName'
        agg_df = pd.merge(agg_stats_df, agg_winrate_df, on='championName')
        champions = agg_df.set_index('championName').to_dict(orient='index')

        columns = st.columns(len(champions))

        for col, (champ_name, data) in zip(columns, champions.items()):
            col.image(
                f'https://ddragon.leagueoflegends.com/cdn/13.23.1/img/champion/{champ_name}.png')
            col.write(
                f""":yellow[Winrate {data['winrate']:.0f}%] 
                :yellow[KDA :green[{data['kda']:.1f}] :blue[{data['win']:.0f}]W - :red[{data['lose']:.0f}]L] 
                :yellow[Damage {data['totalDamageDealtToChampions']:,.0f}]
                """)

        # NOTE: STATS
        st.write("##")
        st.header("✒️Signature")

        name = player_df['championName'].value_counts().idxmax()
        champion = requests.get(
            f"https://ddragon.leagueoflegends.com/cdn/13.23.1/data/en_US/champion/{name}.json").json()['data'][name]

        l, r = st.columns([1.5, 1])
        with l:
            st.image(
                f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{name}_0.jpg")
        with r:
            st.write(
                f"""<h3 style='font-family: Recoleta-Regular; font-weight: 200; font-size: 1.5rem; text-align: center;color:#ffc300'>{champion['title']}</h3>
                    <h1 style='font-family: Recoleta-Regular; font-weight: 400; font-size: 3rem; text-align: center; color:#ffdd00'>{champion['name']}</h1>""", unsafe_allow_html=True)
            st.write(
                f"""<span style='margin: 0 2rem'>{champion['blurb']}</span>""", unsafe_allow_html=True)
            st.write(f":blue[ROLE:] {', '.join(champion['tags'])}")
