class TimeFormatter:
    @staticmethod
    def format(time_in_seconds, precision):
        time_m, time_s, time_ms = \
            TimeFormatter.get_time_parsed(time_in_seconds, precision)
        if precision != 0:
            format_str = "{}:{s:02}:{" + "ms:0{}".format(precision) + "}"
            return format_str.format(time_m, s=time_s, ms=time_ms)
        else:
            return "{}:{s:02}".format(time_m, s=time_s)

    @staticmethod
    def get_time_parsed(time_in_seconds, precision):
        time_m = int(time_in_seconds // 60)
        time_s = int(time_in_seconds - time_m * 60)
        time_ms = int(round((time_in_seconds - time_s - time_m * 60) *
                            pow(10, precision)))
        return time_m, time_s, time_ms
