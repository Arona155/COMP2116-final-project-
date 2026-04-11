import pygame

from config import resource_path

_sound_manager = None


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.menu_bgm_path = resource_path("assets/sound/bgm.mp3")
        self.ingame_bgm_path = resource_path("assets/sound/ingamebgm.mp3")
        self.load_all_sounds()

    def load_all_sounds(self):
        try:
            sound_path = resource_path("assets/sound/laser.wav")
            self.sounds["shoot"] = pygame.mixer.Sound(str(sound_path))
            self.sounds["shoot"].set_volume(1.0)
            return True

        except (pygame.error, FileNotFoundError) as e:
            print(f"Sound load failed: {e}")
            print("Game will run without sound")
            return False

    def play(self, sound_name, loops=0):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play(loops=loops)
            return True
        return False

    def stop(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].stop()

    def play_music(self, music_path, loops=-1, restart=False, volume=0.6):
        if not pygame.mixer.get_init():
            return False

        try:
            if restart:
                pygame.mixer.music.stop()
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=loops)
            return True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Music load/play failed: {e}")
            return False

    def stop_music(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def play_menu_music(self, restart=False):
        return self.play_music(self.menu_bgm_path, loops=-1, restart=restart, volume=0.6)

    def play_ingame_music(self, restart=False):
        return self.play_music(self.ingame_bgm_path, loops=-1, restart=restart, volume=0.6)


def get_sound_manager():
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
