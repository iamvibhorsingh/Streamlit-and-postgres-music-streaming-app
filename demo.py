import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()
    
    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #E9FFFE;
    }
   .sidebar .sidebar-content {
        background-color: #E9FFFE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

'## Read tables'
sql_all_table_names = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
all_table_names = query_db(sql_all_table_names)['relname'].tolist()
table_name = st.selectbox('Choose a table', all_table_names)
if table_name:
    f'{table_name} table looks like:'

    sql_table = f'select * from {table_name};'
    df = query_db(sql_table)
    st.dataframe(df)

'## Query to see detail of a song in the database'
sql_song_title = 'select title from songs;'
song_title = query_db(sql_song_title)['title'].tolist()
song_title = list(set(song_title))
song_title = st.sidebar.selectbox('Choose a song', song_title)
if song_title:
    sql_song = f"select * from songs where title = '{song_title}';"
    song_info = query_db(sql_song).loc[0]
    s_rating, s_duration = song_info['rating'], song_info['duration']
    st.write(f"{song_title} is {s_duration} milliseconds long, and has a rating of {song_info['rating']}.")


'## Query to see detail of a podcast in the database'
sql_podcast_title = 'select title from podcasts;'
podcast_title = query_db(sql_podcast_title)['title'].tolist()
podcast_title = list(set(podcast_title))
podcast_title = st.sidebar.selectbox('Choose a podcast', podcast_title)
if podcast_title:
    sql_podcast = f"select * from podcasts where title = '{podcast_title}';"
    podcast_info = query_db(sql_podcast).loc[0]
    s_broadcaster, s_duration = podcast_info['broadcaster'], podcast_info['duration']
    st.write(f"{podcast_title} is {s_duration} milliseconds long, and is hosted by of {podcast_info['broadcaster']}.")

'## Query to see detail of a playlist in the database'
sql_playlist_title = 'select title from playlists;'
playlist_title = query_db(sql_playlist_title)['title'].tolist()
playlist_title = list(set(playlist_title))
playlist_title = st.sidebar.selectbox('Choose a playlist', playlist_title)
if playlist_title:
    sql_playlist = f"select * from playlists where title = '{playlist_title}';"
    playlist_info = query_db(sql_playlist).loc[0]
    p_creator, p_number = playlist_info['creator'], playlist_info['number_songs']
    st.write(f"{playlist_title} was made by {p_creator}, and has {p_number} songs.")

'## Query for All artists featured in a selected song'
sql_song_info = 'select song_id, title from songs;'
song_info = query_db(sql_song_info)
song_ids, song_names = song_info['song_id'].tolist(), song_info['title'].tolist()
song_id_names = [a + ' : ' + str(b) for a,b in zip(song_names,song_ids)]
song = st.sidebar.multiselect('Choose song (song name : song ID) to look for',song_id_names)


if song:
    songs_id = [a.split(':')[1].strip() for a in song]
    song_id_str = ', '.join(["'" + str(elem) + "'" for elem in songs_id])

    sql_query = f"""select S.title, A.name 
                    from songs as S, artists as A 
                    where S.song_id in ({song_id_str})
                    AND S.song_id = A.song_id
                    group by 1,2;"""
    df_query_info = query_db(sql_query)
    if(not df_query_info.empty):
        st.dataframe(df_query_info)
    else:
        st.write('Nothing.')


'## Query to see the average duration of songs according to gender of users'
sql_gender_info_dur = 'select gender from users;'
gender_info_dur = query_db(sql_gender_info_dur)
gender_names_dur = gender_info_dur['gender'].tolist()
gender_names_dur = list(set(gender_names_dur))
gender_names_dur = st.sidebar.multiselect('Choose Gender to look average duration of songs for',gender_names_dur)

if gender_names_dur:
    gender_dura_str = ', '.join(["'" + str(elem) + "'" for elem in gender_names_dur])

    sql_query = f"""select U.gender, AVG(S.duration) as Averagesongs
                    from songs as S, users as U, library as L
                    where U.gender in ({gender_dura_str})
                    and L.song_id = S.song_id
                    and U.user_id = L.user_id
                    group by 1;"""

    df_query_info = query_db(sql_query)
    if(not df_query_info.empty):
        st.dataframe(df_query_info)
    else:
        st.write('Nothing.')

'## Query to see the average number of songs in playlist according to gender of users'
sql_gender_info = 'select gender from users;'
gender_info_num = query_db(sql_gender_info)
gender_names_num = gender_info_num['gender'].tolist()
gender_names_num = list(set(gender_names_num))
gender_names_num = st.sidebar.multiselect('Choose Gender to look number of songs for',gender_names_num)

if gender_names_num:
    gender_str_nums = ', '.join(["'" + str(elem) + "'" for elem in gender_names_num])

    sql_query = f"""select U.gender, AVG(P.number_songs) as Averagesongs
                    from playlists as P, users as U, library as L
                    where U.gender in ({gender_str_nums})
                    and L.playlist_id = P.playlist_id
                    and U.user_id = L.user_id
                    group by 1;"""

    df_query_info = query_db(sql_query)
    if(not df_query_info.empty):
        st.dataframe(df_query_info)
    else:
        st.write('Nothing.')


'## Query for Average duration of podcast for broadcaster'
sql_broadcaster_info = 'select broadcaster_id, name from broadcasters;'
broadcaster_info = query_db(sql_broadcaster_info)
broadcaster_ids, broadcaster_names = broadcaster_info['broadcaster_id'].tolist(), broadcaster_info['name'].tolist()
broadcaster_id_names = [a + ' : ' + str(b) for a,b in zip(broadcaster_names,broadcaster_ids)]
broadcaster = st.sidebar.multiselect('Choose broadcaster (broadcaster name : broadcaster ID) to look for',broadcaster_id_names)

if broadcaster:
    broadcasters_id = [a.split(':')[1].strip() for a in broadcaster]
    broadcaster_id_str = ', '.join(["'" + str(elem) + "'" for elem in broadcasters_id])

    sql_query = f"""select B.name, AVG(P.duration) as averagepodcastduration
                    from broadcasters as B, podcasts as P 
                    where B.broadcaster_id in ({broadcaster_id_str})
                    and B.podcast_id = P.podcast_id
                    group by 1;"""

    df_query_info = query_db(sql_query)
    if(not df_query_info.empty):
        st.dataframe(df_query_info)
    else:
        st.write('Nothing.')


'## Query for Number of songs in playlist of user'
sql_user_info = 'select user_id, name from users;'
user_info = query_db(sql_user_info)
user_ids, user_names = user_info['user_id'].tolist(), user_info['name'].tolist()
user_id_names = [a + ' : ' + str(b) for a,b in zip(user_names,user_ids)]
user = st.sidebar.multiselect('Choose Users (User name: User ID) to look number of songs for',user_id_names)

if user:
    user_id = [a.split(':')[1].strip() for a in user]
    user_id_str = ', '.join(["'" + str(elem) + "'" for elem in user_id])

    sql_query = f"""select L.user_id, P.playlist_id, P.number_songs
                    from playlists P
		    INNER JOIN library L
		    ON L.playlist_id = P.playlist_id
                    AND L.user_id = {user_id_str}
		    ORDER BY 3;"""
    df_query_info = query_db(sql_query)
    if(not df_query_info.empty):
        st.dataframe(df_query_info)
    else:
        st.write('Nothing.')


