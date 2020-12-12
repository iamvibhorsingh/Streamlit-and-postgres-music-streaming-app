drop table if exists users cascade;
drop table if exists podcasts cascade;
drop table if exists songs cascade;
drop table if exists broadcasters cascade;
drop table if exists playlists cascade;
drop table if exists library cascade;
drop table if exists artists cascade;

create table users(
      user_id integer primary key,
      name varchar(1000),
      gender varchar(10),
      library_id integer unique
    );


create table songs(
      song_id varchar(100) primary key,
      title varchar(1000),
      rating integer,
      duration integer
    );


create table artists(
      artist_id varchar(1000),
      name varchar(1000),
      song_id varchar(1000),
      PRIMARY KEY(song_id, artist_id),
      FOREIGN KEY (song_id) REFERENCES songs (song_id)
    );

create table playlists(
      playlist_id integer,
      title varchar(1000),
      song_id varchar(1000),
      number_songs integer,
      creator varchar(1000),
      PRIMARY KEY(playlist_id, song_id),
      FOREIGN KEY (song_id) REFERENCES songs (song_id)
    );

create table podcasts(
      podcast_id varchar(1000) primary key,
      title varchar(1000),
      duration integer
    );

create table broadcasters(
      broadcaster_id varchar(1000),
      name varchar(1000),
      podcast_id varchar(1000),
      PRIMARY KEY(broadcaster_id, podcast_id),
      FOREIGN KEY (podcast_id) REFERENCES podcasts (podcast_id)
    );


create table library(
      library_id integer,
      user_id integer,
      playlist_id integer,
      song_id varchar(1000),
      podcast_id varchar(1000),
      PRIMARY KEY(library_id, playlist_id, song_id, podcast_id),
      FOREIGN KEY (playlist_id, song_id) REFERENCES playlists (playlist_id, song_id),
      FOREIGN KEY (song_id) REFERENCES songs (song_id),
      FOREIGN KEY (podcast_id) REFERENCES podcasts (podcast_id),
      FOREIGN KEY (user_id) REFERENCES users (user_id)
    );
