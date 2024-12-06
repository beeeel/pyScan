# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:54:38 2024

@author: chatGPT
@curator: ezzwh
"""

import time
from py_common import Action

try:
    import winsound  # Windows sound library
    PLATFORM = "Windows"
except ImportError:
    import simpleaudio as sa  # Cross-platform alternative
    PLATFORM = "CrossPlatform"


class beep(Action):
    def __init__(self, filebase):
        super().__init__(filebase)
        self.sequence = []  # List of tuples (sound_type, count)

    def setup(self):
        """Parse the parameters to build the beep/boop sequence."""
        super().setup()
        for key, value in self.parameters.items():
            if key.lower() in ["beep", "boop"]:
                # Handle "once", "twice", and numeric values
                
                if value == "once":
                    count = 1
                elif value == "twice":
                    count = 2
                else:
                    # Assume the first part of the value is a number
                    count = int(value[0])  
                
                sound_type = key
                self.sequence.append((sound_type, count))


    def run(self):
        """Play the beep/boop sequence."""
        super().run()

        for sound_type, count in self.sequence:
            for _ in range(count):
                self.play_sound(sound_type)
                time.sleep(0.2)  # Short pause between sounds

    def play_sound(self, sound_type):
        """Play a beep or boop sound."""
        if PLATFORM == "Windows":
            if sound_type == "beep":
                winsound.Beep(1000, 300)  # 1000 Hz for 300 ms
            elif sound_type == "boop":
                winsound.Beep(600, 300)  # 600 Hz for 300 ms
        else:  # Cross-platform
            if sound_type == "beep":
                frequency = 1000  # 1000 Hz
            elif sound_type == "boop":
                frequency = 600  # 600 Hz
            else:
                raise ValueError(f"Unknown sound type: {sound_type}")

            # Generate tone
            wave_obj = self.generate_tone(frequency, 0.3)
            wave_obj.play().wait_done()

    @staticmethod
    def generate_tone(frequency, duration):
        """Generate a tone using simpleaudio."""
        import numpy as np
        sample_rate = 44100  # Samples per second
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(frequency * t * 2 * np.pi) * 32767  # Sin wave
        audio_data = tone.astype(np.int16)
        return sa.WaveObject(audio_data, 1, 2, sample_rate)
