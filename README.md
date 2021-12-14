# DriveSafe
Using machine learning, this app gives a rough estimate of the safety of a Spotify playlist while driving.

## Machine Learning
The main idea of the whole app is to determine if a playlist, (mainly the songs in the playlist) is safe for driving.\
A good way to solve this problem is by using **Logistic Regression**. Spotify has available for any songs attributes such as *danceability*, *energy* and *loudness* represented as float numbers. These can be used as features in the model. For this, I scrapped the Spotify API Server using *Spotipy* (A lightweight Python library for the Spotify Web API.) for a considerably large amount of songs (about 4600). After categorizing these songs as SAFE(0) of as DANGEROUS(1), I trained the LR model (using the Scikit-Learn LogisticRegresion). Testing the model afterwards yelded an accuracy of 84%.\
For every playlist we compute the percentage of each song and use the arithmetic mean to determine the danger percentage of the said playlist

## Overal architecture
The application connects to the users Spotify Account in order to make the experience more unique. For predicting the danger percentage of a playlists on the other hand, the application connects to a remote server hosted on a Raspberry Pi.

## Front-end: Kivy
For the presentation layer of he application I chose *Kivy* (a free and open source Python framework for developing mobile apps). The GUI is rather modest, we have a search bar, a swiper so the user can see the playlist name, owner and photo, and a *Check* button to check the danger percentage of the selected playlist. For the unique experience of checking your own playlists, I used the OAuth2 Authentification protocol from Spotipy.\
The **flow** of the application basically is that the user types in the search bar whatever playlist they want to search for and under the hood that querry is passed to Spotipy, which in turn yelds a list of playlists. For those playlists we show the picture, name and owner in the Swiper. The user can browse to find the desired playlist and upon finding it they can press the Check button to find out the danger percentage. Upon pressing the Check button, the application sends the playlist ID to the remove server and gets back a double number representing the percentage. The percentage is shown on a different screen, with a Back button which pressed takes the user back to the main screen. This process can be repeated as the users pleases.\
<br>
<img src="/Frontend/AppScreenShot.jpg" width=324 height=643.8 class="center">
<br>
If something happens to the server, the application will treat this gracefully, showing an error screena with a button to reconnect to the server.

## Back-end: Server
The server is hosted on a Linux machine. The server is multi-threaded, for each client, the server recieves the playlist id and using the model that is stored on the server it computes the prediction and sends it to the client. No computation is done on the client side in order to ensure that it runs smoothly (but mainly because buildozer, the program used to compile kivy apps for mobile does not support the scikit-learn module for compilation :) so I had to improvise and it turned into something much more interesting).
### LRUCache
I implemented the `Least Recently Used Cache` data structure to save the results recently computed, so if the user wants to check a playlist multiple times the server doesn't compute the result each time, it just checks the cache. This addition makes the flow of the application run more smoothly, and doesn't really affect the memory on the server-side (currently the cache has a size of 50, a reasonable amount, but it can be scaled as the user base grows). 

