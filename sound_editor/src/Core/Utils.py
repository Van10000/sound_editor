def put_in_bounds(value, left, right):
    return min(max(value, left), right)


def get_wave_states_sum(*wave_states):
    ans = wave_states[0]
    for i in range(1, len(wave_states)):
        ans = ans.get_added(wave_states[i])
    return ans
