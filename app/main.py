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

roles = {
    "Top": "**Top laners** are resilient, versatile players requiring strong mechanical skills, patience, and adaptability to handle diverse matchups and shifting metas. They excel in isolated duels, contribute to split-pushing, and maintain map awareness for teleport plays.",

    "Jungle": "**Junglers** are strategic leaders with excellent map awareness and decision-making skills. They control objectives, gank lanes, counter-jungle, and adapt their tactics based on the flow of the game. Communication and anticipation of the opposing jungler's movements are crucial.",

    "Mid": "**Mid laners** are playmakers with mechanical prowess, map awareness, and game knowledge. They farm minions, roam, and excel in burst or control champions. Vision control, positioning, and understanding matchups are vital for success.",

    "Adc": "**Adc players** provide consistent damage in team fights, relying on positioning and mechanical skill. They navigate the laning phase safely, farm efficiently, and synergize with their support for trades and kills. Map awareness helps them avoid ganks and rotations.",

    "Support": "**Support** players offer utility, vision control, and protection for their team. They excel in map awareness, communication, and adaptability, adjusting their playstyles and item builds as needed. Positioning and timing are crucial for landing crowd control and protecting carries."
}


# TODO: Main
_, center, _ = st.columns([1, 10, 1])
with center:
    st.markdown("""
                <h1 style='
                font-family: "Inconsolata"; font-weight: 400; color: #ffc300;
                font-size: 3.5rem'>How Bad Is Your League</h1>""",
                unsafe_allow_html=True)
    st.markdown("""<h3 style='
                font-family: "Inconsolata"; font-weight: 400;
                font-size: 1.5rem'>Our sophisticated A.I. judges your awful gameplay</h3>""",
                unsafe_allow_html=True)
    """
    ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=fafafa)
    ![Plotly](https://img.shields.io/badge/plotly%20-%2300416A.svg?&style=for-the-badge&logo=pandas&logoColor=white)
    ![Riot Games](https://img.shields.io/badge/riotgames-D32936.svg?style=for-the-badge&logo=riotgames&logoColor=white)
    """
    st.image("img/poros.jpg")

    st.subheader("🔒Team info is locked",  help="Admin only")
    password = st.text_input(
        "Enter password to unlock team info", type="password")

    st.subheader("🔍Search summoner")
    with st.form("summoner"):
        st.markdown("Fill out your summoner information")
        l, r = st.columns([2, 1])
        with l:
            name = st.text_input(
                "Enter summoner name", "Obiwan", key="name")
        with r:
            tag = st.text_input(
                "Enter tagline", "HYM")
        region = st.selectbox(
            'Choose your region',
            ('VN2', 'OC1'), index=None)
        games = st.slider('Number of matches', 5, 30, 15)
        if region == 'OC1':
            mode = st.selectbox(
                'Choose game mode',
                ('Ranked Solo', 'Normal Draft'), index=None)
        else:
            mode = st.selectbox(
                'Choose game mode',
                ('Ranked Solo', 'Ranked Flex', 'Quick Play', 'Normal Draft'), index=None)
        run = st.form_submit_button("Find out")

if password == "HYM":
    # NOTE: TEAM RANKED
    st.write("##")
    with open('team.json', 'r') as f:
        team = json.load(f)
    _, center, _ = st.columns([1, 10, 1])
    with center:
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
                data = df.groupby('summonerName')[
                    'visionScore'].mean().to_dict()
                fig = graph_vision(data)
                st.plotly_chart(fig, use_container_width=True)
            with r:
                st.subheader("What's a good vision score?")
                st.write(
                    "A good vision score is `1.5x` the game length, a great vision score is more in the `2x` ballpark.")
                st.write("That doesn't mean just spam wards everywhere because a high vision score does nothing if you don't have good vision on things that **MATTER**.")
                fig = graph_winrate_by_side(df)
                st.plotly_chart(fig, use_container_width=True)

if run:
    if region is None:
        raise MissingRegionError("Please choose your region")
    if mode is None:
        raise MissingQueueError("Please choose game mode")
    queues = {
        "Ranked Flex": 440,
        "Ranked Solo": 420,
        "Quick Play": 490,
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
        league_of_graph = f"https://www.leagueofgraphs.com/summoner/{'vn' if region == 'VN2' else 'oce'}/{name}-{tag}"

        ids = get_match_ids(TOKEN, puuid, games, queue_id)
    except KeyError:
        _, center, _ = st.columns([1, 10, 1])
        with center:
            st.error("🍎Summoner not found")
    else:
        _, center, _ = st.columns([1, 10, 1])
        with center:
            with st.spinner(f"⌛Extracting data for `{name}`"):
                match_df, player_df = gather_data(TOKEN, puuid, ids)
                stats = transform(match_df, player_df)
        # NOTE: PROFILE
        st.write("##")
        _, l, r, _ = st.columns([0.5, 1, 4, 0.5])
        with l:
            st.image(
                f"https://ddragon.leagueoflegends.com/cdn/13.23.1/img/profileicon/{summoner['profileIconId']}.png", width=250)
            st.link_button("Summoner Profile",
                           f"https://www.op.gg/summoners/{'vn' if region == 'VN2' else region}/{name}-{tag}")
        with r:
            _, a, b, _ = st.columns([1, 2, 2, 1])
            with a:
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
                    f"`Level`: {summoner['summonerLevel']}")
                st.write(f"`LP`: {ranks['leaguePoints']}")
                st.write(f"`Winrate`: {((wins/(wins+losses))*100):.1f}%")
            with b:
                st.markdown("##")
                st.markdown("##")
                st.image(f"img/rank/{ranks['tier']}.png", width=250)

        # NOTE: MOST USED CHAMPS
        _, center, _ = st.columns([1, 10, 1])
        with center:
            st.write("##")
            st.subheader("🏆Victorious lineup")
            stat = ['totalDamageDealtToChampions',
                    'kills', 'deaths', 'assists']

            # Create a DataFrame with the aggregated data
            agg_stats_df = player_df.groupby('championName')[stat].mean()
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
            champions = agg_df.set_index(
                'championName').to_dict(orient='index')

            columns = st.columns(5)

            for idx, (col, (champ_name, data)) in enumerate(zip(columns, champions.items())):
                if idx < 5:
                    col.image(
                        f'https://ddragon.leagueoflegends.com/cdn/13.23.1/img/champion/{champ_name}.png')
                    col.write(f""":yellow[Winrate {data['winrate']:.0f}%] 
                                    :yellow[KDA :green[{data['kda']:.1f}] :blue[{data['win']:.0f}]W - :red[{data['lose']:.0f}]L] 
                                    :yellow[Damage {data['totalDamageDealtToChampions']:,.0f}]
                                    """)
                else:
                    break

            # NOTE: SIGNATURE CHAMP
            st.write("##")
            st.subheader("✨Signature champion")

            name = player_df['championName'].value_counts().idxmax()
            champion = requests.get(
                f"https://ddragon.leagueoflegends.com/cdn/13.23.1/data/en_US/champion/{name}.json").json()['data'][name]

            l, r = st.columns([1, 1])
            with l:
                st.image(
                    f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{name}_0.jpg")
            with r:
                st.write(f"""
                        <h3 style='font-family: Recoleta-Regular; font-weight: 200; font-size: 2rem; text-align: center;color:#ffc300'>{champion['name']}</h3>
                        """, unsafe_allow_html=True)
                st.markdown(f"{champion['blurb']}")
                st.markdown(f"`Title`: {champion['title']}")
                st.markdown(f"`Role`: {', '.join(champion['tags'])}")

            # NOTE: STATS
            st.write("##")
            st.subheader(f"📑Nexus insights")
            columns_data = {
                "🎯Games": f"{stats['wins'] + stats['loses']}G {stats['wins']}W {stats['loses']}L",
                "🏆Winrates": f"{(stats['wins'] / (stats['wins'] + stats['loses'])) * 100:.1f} %",
                "⚔️KDA": f"{stats['kills']:.1f}/{stats['deaths']:.1f}/{stats['assists']:.1f}",
                "🥊Damage": f"{stats['dmg']:,.0f}",
                "👑Pentakills": stats['penta'],
                "👁️Vision": f"{stats['vision']:.1f}",
                "🧑‍🌾CSperMin": stats['cspermin'],
                "🥷Objectives": f"Max {stats['objsStolen']} stolen",
                "👩‍🚀Time Alive": f"Longest {int(stats['timealive'])} min"
            }

            for i in range(0, len(columns_data), 3):
                l, m, r = st.columns([1, 1, 1])
                with l:
                    title, value = list(columns_data.items())[i]
                    st.subheader(title)
                    st.subheader(value)
                with m:
                    title, value = list(columns_data.items())[i + 1]
                    st.subheader(title)
                    st.subheader(value)
                with r:
                    title, value = list(columns_data.items())[i + 2]
                    st.subheader(title)
                    st.subheader(value)

        # NOTE: GRAPHS
            st.markdown("##")
            l, r = st.columns([1, 1])
            with l:
                st.markdown("<span style='font-weight: 800;font-size: 25px'>Roles and Winrates</span>",
                            unsafe_allow_html=True)
                fig, role = graph_role_dist(player_df)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(roles[role])
            with r:
                st.markdown("##")
                st.markdown("##")
                fig = graph_winrate_by_role(player_df)
                st.plotly_chart(fig, use_container_width=True)
                fig = graph_winrate_by_side(player_df)
                st.plotly_chart(fig, use_container_width=True)
                st.link_button("League of Graphs", league_of_graph)

            # Lane stats
            st.markdown("##")
            fig = graph_personal(match_df, player_df)
            st.plotly_chart(fig, use_container_width=True)

            # Gold by damage
            fig = graph_dmgpersonal(match_df, player_df)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
                        ### ⭐ Star the project on Github <iframe src="https://ghbtns.com/github-btn.html?user=nauqh&repo=porobot&type=star&count=true" width="150" height="20" title="GitHub"></iframe>
                        """, unsafe_allow_html=True)


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
