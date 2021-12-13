import hashlib
import socket

import kivy
import spotipy
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.swiper import MDSwiper, MDSwiperItem

from Frontend.FrontendUtils import ServerPlaylistAnalysis, searchResultsPlaylists

SPOTIFY_CLIENT_ID = '0fcd6809776648a39887d531b7c31653'
SPOTIFY_CLIENT_SECRET = 'aa476771bb4b4a96a8f5f648a39e3ef3'

kivy.require('2.0.0')


class DriveSafe(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Actual server -> 172.105.98.9
        self.swiperItems = []
        self.server_address = ('192.168.100.4', 6969)
        self.tracks = {}
        self.screen_manager = ScreenManager()
        self.MainScreen = MDScreen(name='main', r=25 / 255, g=20 / 255, b=20 / 255)
        self.table_elements = []
        self.spotify = spotipy.Spotify(
            client_credentials_manager=spotipy.SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
        scope = "user-library-read"
        self.spotify = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                                              redirect_uri="http://localhost:8080", scope=scope))

        self.title_label = MDLabel(
            text="[size=24][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-Bold]DriveSafe for [b]Spotify[/b][/font]["
                 "/color][/size]",
            markup=True,
            halign="left",
            size_hint=(1, 0.1)
        )

        self.swiper = MDSwiper(
            size_hint=(0.9, 0.6),
        )

        self.searchInput = TextInput(hint_text="Search a playlist...", size_hint=(0.75, 0.6), multiline=False)
        self.searchButton = MDRaisedButton(
            text="[size=24][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-SemiBold]Search[/font][/color][/size]",
            size_hint=(0.25, 0.6),
            md_bg_color=(1, 1, 1, 1)
        )

        self.backButton = MDFillRoundFlatButton(
            text="[size=24][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-SemiBold]Back[/font][/color][/size]",
            pos_hint={"center_x": .5, "center_y": .25},
            size_hint=(0.3, 0.2),
            md_bg_color=(1, 1, 1, 1)
        )

        self.checkButton = MDFillRoundFlatButton(
            text="[size=24][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-SemiBold]Check[/font][/color][/size]",
            pos_hint={"center_x": .5, "center_y": .25},
            size_hint=(0.3, 0.1),
            md_bg_color=(1, 1, 1, 1)
        )

        self.ResultScreen = MDScreen(name='result', r=25 / 255, g=20 / 255, b=20 / 255)

        self.ConnectionErrorScreen = MDScreen(name='connect-error', r=25 / 255, g=20 / 255, b=20 / 255)
        self.reconnectButton = MDFillRoundFlatButton(
            text="[size=24][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-SemiBold]Reconnect[/font][/color][/size]",
            pos_hint={"center_x": .5, "center_y": .25},
            size_hint=(0.3, 0.2),
            md_bg_color=(1, 1, 1, 1)
        )

        self.connectionErrorLabel = MDLabel(
            pos_hint={"center_x": .5, "center_y": .75},
            text="[size=48][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-Bold]Connection to server failed[/font][/color][/size]",
            markup=True,
            halign="center",
            size_hint=(1, 0.1)
        )

        self.resultLabel = MDLabel(
            pos_hint={"center_x": .5, "center_y": .75},
            text="[size=48][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-Bold] ...[/font][/color][/size]",
            markup=True,
            halign="center",
            size_hint=(1, 0.1)
        )

    def establishConnection(self, garbage=None):
        try:
            self.server.connect(self.server_address)
            self.screen_manager.current = 'main'
        except ConnectionRefusedError:
            self.screen_manager.current = 'connect-error'

    def build(self):
        # Define Screen
        layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))
        searchLayout = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.1), height=150)
        searchLayout.add_widget(self.searchInput)
        searchLayout.add_widget(self.searchButton)
        layout.add_widget(self.title_label)
        layout.add_widget(searchLayout)
        layout.add_widget(self.swiper)
        layout.add_widget(self.checkButton)
        self.MainScreen.add_widget(layout)

        reslayout = FloatLayout()
        reslayout.add_widget(self.backButton)
        reslayout.add_widget(self.resultLabel)
        self.ResultScreen.add_widget(reslayout)

        errorLayout = FloatLayout()
        errorLayout.add_widget(self.reconnectButton)
        errorLayout.add_widget(self.connectionErrorLabel)
        self.ConnectionErrorScreen.add_widget(errorLayout)

        self.searchButton.bind(on_press=self.search)
        self.backButton.bind(on_press=self.backToMain)
        self.reconnectButton.bind(on_press=self.establishConnection)
        self.checkButton.bind(on_press=self.computeResult)

        self.screen_manager.add_widget(self.MainScreen)
        self.screen_manager.add_widget(self.ResultScreen)
        self.screen_manager.add_widget(self.ConnectionErrorScreen)
        self.establishConnection(None)

        return self.screen_manager

    def search(self, garbage):
        s = self.searchInput.text
        if s != "":
            results = searchResultsPlaylists(self.spotify, s, 50)
            self.table_elements = results.copy()
            for i in self.swiperItems:
                self.swiper.remove_widget(i)
            self.swiperItems = []
            self.swiper.set_current(0)
            self.tracks = {}
            count = 0
            for r in results:
                item = MDSwiperItem(orientation="vertical")
                item.add_widget(AsyncImage(source=r[4], size_hint_y=0.8))
                item.add_widget(MDLabel(
                    text="[size=24][color=#191414][font=Frontend/SpotifyFonts/Montserrat-Regular]" + r[
                        0] + "[/font][/color][/size]", halign="center", size_hint_y=0.2, markup=True))
                item.add_widget(MDLabel(
                    text="[size=24][color=#191414][font=Frontend/SpotifyFonts/Montserrat-Regular]" + r[
                        1] + "[/font][/color][/size]", halign="center", size_hint_y=0.2, markup=True))
                self.swiper.add_widget(item)
                self.swiperItems.append(item)
                self.tracks[count] = r[3]
                count += 1
            # if len(results) == 1:
            #     item = MDSwiperItem(orientation="vertical")
            #     self.swiper.add_widget(item)

    def computeResult(self, garbage=None):
        playlist_id = self.tracks[self.swiper.get_current_index()]
        result = None
        try:
            result = ServerPlaylistAnalysis(self.server, playlist_id)
            if result == -1:
                self.resultLabel.text = "[size=48][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-Bold]" + "Private playlist not currently supported" + "[/font][/color][/size]"
            else:
                result *= 100
                result = str(round(result, 2))
                self.resultLabel.text = "[size=48][color=#1DB954][font=Frontend/SpotifyFonts/Montserrat-Bold]" + \
                                        result + " % \nDangerous[/font][/color][/size]"
            self.screen_manager.current = 'result'
        except Exception as e:
            print(e)
            self.server.close()
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.establishConnection()

    def backToMain(self, garbage):
        self.screen_manager.current = 'main'
