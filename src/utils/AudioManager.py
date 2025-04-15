import pygame


class AudioManager:
    """
    Manages all audio playback in the game, including sound effects and background music.

    This class implements the Singleton design pattern to ensure that only one instance
    of the audio manager exists throughout the entire game.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        pygame.mixer.init()

        self.volume_global_sounds = 1.0
        self.volume_global_music = 1.0

        # Sound effects
        self.sounds = {
            "boom": pygame.mixer.Sound("assets/sounds/boom.wav"),
            "click": pygame.mixer.Sound("assets/sounds/retro_click.wav"),
            "critical shot": pygame.mixer.Sound(
                "assets/sounds/critical_shot.wav"),
            "death": pygame.mixer.Sound("assets/sounds/death.wav"),
            "game over": pygame.mixer.Sound("assets/sounds/game_over.wav"),
            "gun shot": pygame.mixer.Sound("assets/sounds/gun_shot.wav"),
            "hit": pygame.mixer.Sound("assets/sounds/hit.wav"),
            "launcher": pygame.mixer.Sound("assets/sounds/launcher.wav"),
            "laser beam": pygame.mixer.Sound("assets/sounds/laser_beam.wav"),
            "laser shot": pygame.mixer.Sound("assets/sounds/laser_shot.wav"),
            "plasma": pygame.mixer.Sound("assets/sounds/plasma.wav"),
            "recharged": pygame.mixer.Sound("assets/sounds/recharged.wav"),
            "stomp": pygame.mixer.Sound("assets/sounds/stomp.wav")
        }

        # Base volume for each sound
        self.base_volumes = {
            "boom": 1,
            "click": 0.9,
            "critical shot": 0.2,
            "death": 0.1,
            "game over": 0.3,
            "gun shot": 0.2,
            "hit": 0.5,
            "launcher": 0.5,
            "laser beam": 0.1,
            "laser shot": 0.2,
            "plasma": 0.5,
            "recharged": 0.2,
            "stomp": 0.3
        }

        self.songs = {
            "play": "assets/sounds/soundtrack.mp3"
        }

        self.base_music_volumes = {
            "play": 0.2,
        }

        self.current_music_name = None
        self.update_sounds_volume()

    def play_sound(self, sound_name: str):
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()

    def play_music(self, music_name: str, loop: int = -1):
        if self.current_music_name == music_name:
            return
        path = self.songs.get(music_name)
        if path:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loop)
            self.current_music_name = music_name
            self.update_music_volume()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music_name = None

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def update_sounds_volume(self):
        for name, sound in self.sounds.items():
            base = self.base_volumes.get(name, 1.0)
            sound.set_volume(base * self.volume_global_sounds)

    def update_music_volume(self):
        if self.current_music_name:
            base = self.base_music_volumes.get(self.current_music_name, 1.0)
            pygame.mixer.music.set_volume(base * self.volume_global_music)

    def set_sounds_volume(self, volume: float):
        self.volume_global_sounds = volume
        self.update_sounds_volume()

    def set_music_volume(self, volume: float):
        self.volume_global_music = volume
        pygame.mixer.music.set_volume(volume)
