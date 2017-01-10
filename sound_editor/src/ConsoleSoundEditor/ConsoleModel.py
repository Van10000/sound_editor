import functools
import os

from ConsoleSoundEditor.NamedTrack import NamedTrack
from Core.WaveState.Loudness import Loudness
from Core.WaveState.WaveState import WaveState
from ViewModel.ViewUtils.TimeFormatter import TimeFormatter


class ConsoleModel:
    def __init__(self):
        self.tracks = []
        self.dir = None

    def set_path(self, path):
        self.dir = path
        return "Path was set to {}".format(path)

    def get_all_tracks_names(self):
        names = [track.name for track in self.tracks]
        return ("There are the following tracks active:\n"
                "{}").format("\n".join(names))

    def get_track_with_exception(self, name):
        """
        :rtype: WaveState
        """
        track = self.get_track(name)
        if track is None:
            raise Exception("There is no track with name {}".format(name))
        return track

    def get_tracks_with_exception(self, *names):
        tracks = list(map(self.get_track, names))
        for name, track in zip(names, tracks):
            if track is None:
                raise Exception("There is no track with name {}".format(name))
        return tracks

    def get_named_track(self, name):
        for track in self.tracks:
            if track.name == name:
                return track

    def get_named_track_with_exception(self, name):
        named_track = self.get_named_track()
        if named_track is None:
            raise Exception("There is no track with name {}".format(name))

    def get_track(self, name):
        """
        :rtype: WaveState
        """
        named_track = self.get_named_track(name)
        return None if named_track is None else named_track.wave_state

    def rename_track(self, name, new_name):
        for track in self.tracks:
            if track.name == name:
                track.name = new_name
                return "Track {} was renamed to {}".format(name, new_name)

    def get_next_name(self):
        for i in range(len(self.tracks) + 1):
            if self.get_track(str(i)) is None:
                return str(i)

    def add_track(self, wave_state, name=None):
        if name is None:
            name = self.get_next_name()
        track_by_name = self.get_track(name)
        if track_by_name is None:
            self.tracks.append(NamedTrack(name, wave_state))
        else:
            raise NameError("Name {} is already taken".format(name))
        return name

    def open(self, filename, result_name=None):
        if self.dir is not None:
            filename = os.path.join(self.dir, filename)
        track = WaveState.read_from_file(filename)
        result_name = self.add_track(track, result_name)
        return ("File {} was opened.\n"
                "Result is at {}").format(filename, result_name)

    def save(self, name, filename):
        if self.dir is not None:
            filename = os.path.join(self.dir, filename)
        track = self.get_track_with_exception(name)
        track.save_to_file(filename)
        return "Track {} was saved to file {}".format(name, filename)

    def part(self, name, start_time, end_time, result_name=None):
        track = self.get_track_with_exception(name)
        start_sample = ConsoleModel._get_sample_number(track, start_time)
        end_sample = ConsoleModel._get_sample_number(track, end_time)
        part = track.get_part(start_sample, end_sample)
        result_name = self.add_track(part, result_name)
        return ("Part of {} was taken.\n"
                "Result is at {}").format(name, result_name)

    def join(self, *names, result_name=None):
        tracks = self.get_tracks_with_exception(*names)
        result_track = functools.reduce(WaveState.get_appended, tracks)
        result_name = self.add_track(result_track, result_name)
        names_str = ", ".join(names)
        return ("Tracks {} were joined.\n"
                "Result is at {}").format(names_str, result_name)

    def insert(self, base_track_name, insert_track_name,
               time, result_name=None):
        base_track, put_track = self.get_tracks_with_exception(
            base_track_name, insert_track_name)
        sample = self._get_sample_number(base_track, time)
        result_track = base_track.get_inserted(put_track, sample)
        result_name = self.add_track(result_track, result_name)
        return ("Track {} was inserted in track {} from time {}.\n"
                "Result is at {}").format(base_track_name, insert_track_name,
                                          time, result_name)

    def delete(self, name, start_time, end_time, result_name=None):
        track = self.get_track_with_exception(name)
        start_sample = ConsoleModel._get_sample_number(track, start_time)
        end_sample = ConsoleModel._get_sample_number(track, end_time)
        result_track = track.get_with_deleted_part(start_sample,
                                                   end_sample)
        result_name = self.add_track(result_track, result_name)
        return ("From track {} was deleted part from {} to {}.\n"
                "Result is at {}").format(name, start_time,
                                          end_time, result_name)

    def delete_track(self, name):
        named_track = self.get_named_track(name)
        self.tracks.remove(named_track)
        return "Track {} was closed.".format(name)

    def fade(self, fade_type, name, result_name=None):
        if fade_type not in ["in", "out"]:
            raise FormatError("Fade type should be either in or out.\n"
                              "Your input: {}".format(fade_type))
        from_start = fade_type == "in"
        wave_state = self.get_track_with_exception(name)
        fade_loudness = Loudness.get_fade(len(wave_state), from_start)
        result_track = wave_state.get_with_changed_loudness(fade_loudness)
        result_name = self.add_track(result_track, result_name)
        return ("Applied fade {} to track {}.\n"
                "Result is at {}.").format(fade_type, name, result_name)

    def change_speed(self, name, ratio, result_name=None):
        ratio = ConsoleModel._parse_ratio(ratio)
        track = self.get_track_with_exception(name)
        if ratio < 0:
            raise FormatError("Ratio should be positive.\n"
                              "Your input: {}".format(ratio))
        result_track = track.get_with_changed_tempo_and_pitch(ratio)
        result_name = self.add_track(result_track, result_name)
        return ("Changed speed in track {} with ratio {}.\n"
                "Result is at {}").format(name, ratio, result_name)

    def reverse(self, name, result_name=None):
        track = self.get_track_with_exception(name)
        result_track = track.get_reversed()
        result_name = self.add_track(result_track, result_name)
        return ("Reversed track {}.\n"
                "Result is at {}").format(name, result_name)

    def get_sum(self, *names, result_name=None):
        tracks = self.get_tracks_with_exception(*names)
        result_track = functools.reduce(WaveState.get_added, tracks)
        result_name = self.add_track(result_track, result_name)
        names_str = ", ".join(names)
        return ("Tracks {} were summed.\n"
                "Result is at {}").format(names_str, result_name)

    def change_loudness(self, name, ratio, result_name=None):
        ratio = ConsoleModel._parse_ratio(ratio)
        if ratio < 0:
            raise FormatError("Ratio should be positive.\n"
                              "Your input: {}".format(ratio))
        track = self.get_track_with_exception(name)
        loudness = Loudness.get_constant_loudness(len(track), ratio)
        result_track = track.get_with_changed_loudness(loudness)
        result_name = self.add_track(result_track, result_name)
        return ("Changed loudness in track {} with ratio {}.\n"
                "Result is at {}").format(name, ratio, result_name)

    def compress(self, name, ratio, result_name=None):
        ratio = ConsoleModel._parse_ratio(ratio)
        if ratio < 0 or ratio > 1:
            raise FormatError("Ratio should be between 0 and 1.\n"
                              "Your input: {}".format(ratio))
        track = self.get_track_with_exception(name)
        result_track = SoundCompressor.compress(track, ratio)
        result_name = self.add_track(result_track, result_name)
        return ("Compressed track {} with ratio {}.\n"
                "Result is at {}").format(name, ratio, result_name)

    @staticmethod
    def _get_sample_number(wave_state, time):
        if time == "end":
            return len(wave_state)
        time_parsed = ConsoleModel._parse_time_to_seconds(time)
        wave_state_len = len(wave_state) / wave_state.frame_rate
        if wave_state_len < time_parsed:
            wave_state_len = TimeFormatter.format(wave_state_len, 6)
            raise FormatError("Too big time given.\n"
                              "Track length is {}\n".format(wave_state_len) +
                              "Your input is {}".format(time))
        if time_parsed < 0:
            raise FormatError("Time should be positive.\n"
                              "Your input is {}".format(time))
        return int(round(time_parsed * wave_state.frame_rate))

    @staticmethod
    def _parse_time_to_seconds(time):
        time_format_error = FormatError("Time format should be mm:ss:ms.\n"
                                        "Your input:{}".format(time))
        time_parts = time.split(':')
        if len(time_parts) > 3:
            raise time_format_error
        while len(time_parts) < 3:
            time_parts.append("0")
        try:
            return (float(time_parts[0]) * 60 +
                    float(time_parts[1]) +
                    float("0." + time_parts[2]))
        except ValueError:
            raise time_format_error

    @staticmethod
    def _parse_ratio(ratio):
        try:
            return float(ratio)
        except ValueError:
            return FormatError("Ratio should be a decimal number."
                               "Your input is {}".format(ratio))


class FormatError(Exception):
    pass
