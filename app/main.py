import streamlit as st
from utils.config import settings
from utils.riot import *
from utils.graph import *
import pandas as pd


st.set_page_config(
    page_title="Porostream",
    page_icon="img/favicon.png",
    layout="wide")

puuids = {
    'Thánh Chặt Xác': '8UIhStkspIglog9paowA4mXzlckT-xySwWNIFac3o2ojumva9ffkFMda_jGpW_hhInKWpvUp5pPPrA',
    'Cozy Bearrrrr': 'mh3B8Naz1MbJ6RE7dJTu3ZCLh7Rwo6CCJQiA-fVlLXUuQmkibMVMztpCLALJMMJQm4QOevN1-u0lnA',
    'indestructibleVN': 'DV0Aad31H16g3lItoojolWMPZQYOj0l90KzVSUV-qF3QlF92hOC_WLLssdR1MqPS-3UMEKp0Mn5woA',
    'Obiwan': 'aTa5_43m0w8crNsi-i9nxGpSVU06WZBuK-h9bZEOK0g_lJox3XF4Dv4BzVwZieRj0QwlGnJ4SZbftg',
    'Wavepin': 'idASdW5eSrO5Oih-ViK07RdeXE33JM1Mm3FwV7JiveTwbqfjl1vQUvToJ95c1B4EeQd8BAZgXkGSUw'
}

if "run" not in st.session_state:
    st.session_state['run'] = False


def click_run():
    st.session_state['run'] = True


# TODO: Sidebar
with st.sidebar:
    st.write("## 📝About the project")
    st.markdown(
        "Porostream lets you analyze your League of Legends history to give you a deeper understanding of your performance.")
    st.markdown(
        "Status: Beta")

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

# NOTE: LEADERBOARD
df = pd.read_csv("matches.csv")

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

# NOTE: SEARCH INPUT
with st.sidebar:
    st.header("🔍Search summoner")
    url = st.text_input(
        "Enter summoner name and tag", "Obiwan, #HYM")
    option = st.selectbox(
        'Choose your region',
        ('Asia', 'Europe', 'North America', 'Oceania'))
    mode = st.multiselect(
        'Choose game mode',
        ['Normal', 'Ranked Flex', 'Aram', 'Nexus Blizt'],
        ['Ranked Flex'])

    st.header("🔒B.R.O")
    summoner = st.selectbox(
        'Choose summoner',
        ('Thánh Chặt Xác', 'Cozy Bearrrrr', 'indestructibleVN', 'Obiwan', 'Wavepin', 'Tupac Shaco'), index=None)

    run = st.button("Find out", on_click=click_run)


if run or st.session_state['run']:
    TOKEN = settings.TOKEN
    try:
        puuid = puuids[summoner]
    except Exception:
        st.subheader("💀Summoner has not been added")
        st.write("Submit a form to add your summoner")
        with st.form("my_form"):
            key = st.text_input(
                "Enter RIOT API key (optional)", "")
            l, r = st.columns([1, 1])
            with l:
                url = st.text_input(
                    "Enter summoner name and tag", "Obiwan, #HYM")
            with r:
                option = st.selectbox(
                    'Choose your region',
                    ('Asia', 'Europe', 'North America', 'Oceania'))
            game = st.multiselect(
                'Choose game mode',
                ['Normal', 'Ranked Flex', 'Aram', 'Nexus Blizt'],
                ['Ranked Flex', 'Nexus Blizt'])
            slider_val = st.slider(
                "Number of games", min_value=0, max_value=20, value=10)
            checkbox_val = st.checkbox("Permission for using summoner data")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.success("✅ Submitted application")

    else:
        st.subheader("⌛Extracting data from RIOT API")

        summoner, name = get_info(TOKEN, puuid)
        ids = get_match_ids(TOKEN, puuid, 10, queue_id=440)
        match_df, player_df = gather_data(TOKEN, puuid, ids)

        stats = transform(match_df, player_df)

        # NOTE: PROFILE
        st.write("##")
        l, r = st.columns([1, 2])
        with l:
            st.image(
                f"https://ddragon.leagueoflegends.com/cdn/13.23.1/img/profileicon/{summoner['profileIconId']}.png")
        with r:
            st.write("""<span style='
                    font-weight: 200; font-size: 1rem'>SUMMONER PROFILE</span>""",
                     unsafe_allow_html=True)
            st.write(f"""<span style='
                    font-family: Recoleta-Regular; font-weight: 400;
                    font-size: 3rem'>{name['gameName']}</span>""",
                     unsafe_allow_html=True)
            st.write(f"`Level`: {summoner['summonerLevel']}")
            st.write(f"`Tagline`: {name['tagLine']}")

        # NOTE: STATS
        st.header("Summoner stats")
        l, m, r = st.columns([1, 1, 1])
        with l:
            st.header("🎯Games")
            st.subheader(
                f"{stats['wins'] + stats['loses']}G {stats['wins']}W {stats['loses']}L")
        with m:
            st.header("🏆Winrates")
            st.subheader(f"{round((stats['wins']/10), 2)*100} %")
        with r:
            st.header("⚔️KDA")
            st.subheader(
                f"{stats['kills']}/{stats['deaths']}/{stats['assists']}")

        l, m, r = st.columns([1, 1, 1])
        with l:
            st.header("🥊Damage")
            st.subheader(stats['dmg'])
        with m:
            st.header("Pentakills")
            st.subheader(stats['penta'])
        with r:
            st.header("💡Vision")
            st.subheader(stats['vision'])
