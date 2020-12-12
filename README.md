### The project was to design and develop an application, using Postgres database, for getting various insights about different parts of audio streaming components like users, songs, podcasts etc. The tables in the design can be used perform queries on all the components of our system.


### Data source
For  data acquisition,  real-world data from a web API called Exportify (that uses Spotify's API) was consumed and then loaded it into a csv file and pre-processed.

### Business rules
- Library - it is the library of a user
-- A library belongs to exactly one user
- User - users of the application
-- A user has exactly one library
- Songs - songs in our music database
- Artists - artists in our music database
-- An artist has at least one song
- Playlist
-- A playlist has at least one song
- Podcast – podcasts in our database
- Broadcaster - broadcasters in our database
-- A broadcaster has at least one podcast

### Examples of kinds of queries that can be done
- Query to see detail of a song in the database
- Query to see detail of a podcast in the database
- Query to see detail of a playlist in the database
- All artists featured in a selected song
- See average duration of songs according to gender of users
- See average number of songs in playlist according to gender of users
- Average duration of podcast for broadcaster
- Number of songs in playlist of user
