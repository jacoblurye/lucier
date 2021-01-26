from lucier import Sequencer, MidiController, utils

one = utils.random_sequences(
    [
        [52 - 12, 66 - 12, 73 - 12, 75 - 12, 73 - 12],
        [64 - 12, 61 - 12, 75 - 12, 61 - 12],
    ]
)
two = utils.random_sequences(
    [
        [54 - 12, 66 - 12, 73 - 12, 76 - 12, 73 - 12],
        [75 - 12, 76 - 12, 75 - 12, 76 - 12],
        [66 - 12, 61 - 12, 75 - 12, 61 - 12],
    ]
)
maybe_8va = utils.random_iter([0] * 5 + [12])
hits = set([52, 54])

s = Sequencer(tps=50)


@s.register([MidiController(c) for c in range(3)])
async def dots(ctrl: MidiController, tick: int):
    if utils.every_n_ticks(2, tick, offset=ctrl.channel * 10) and utils.coin_flip(0.4):
        down_8ba = next(maybe_8va)
        note = (next(two) if (tick % 500) > 250 else next(one)) - down_8ba - down_8ba
        await ctrl.play_note(note, utils.r.randint(40, 70), 0.1 if down_8ba == 0 else 5)

    if utils.every_n_ticks(25, tick):
        ctrl.set_cc(9, utils.r.randint(30, 87))
        ctrl.set_cc(1, utils.r.randint(10, 50))


@s.register([MidiController(c) for c in range(3, 9)])
async def sighs(ctrl: MidiController, tick: int):
    if (
        utils.every_n_ticks(50, tick, offset=ctrl.channel * 10)
        and utils.coin_flip(0.80)
    ) or utils.coin_flip(0.1):
        note = (
            (next(two) if (tick % 480) > 240 else next(one))
            + next(maybe_8va)
            + next(maybe_8va)
        )
        await ctrl.play_note(note, utils.r.randint(40, 70), 3)

    if utils.every_n_ticks(25, tick + utils.r.randint(0, 15)):
        ctrl.set_cc(1, abs(tick % 7 - tick % 5 - tick % 3 + tick % 2) * 5)
        ctrl.set_cc(11, abs(tick % 7 - tick % 5 - tick % 3 + tick % 2) * 5)


@s.register([MidiController(9)])
async def drum(ctrl: MidiController, tick: int):
    if utils.every_n_ticks(8, tick):
        note = next(two) if (tick % 500) > 250 else next(one)
        if note in hits:
            await ctrl.play_note(note, utils.r.randint(40, 70), 5)

    if utils.every_n_ticks(25, tick):
        ctrl.set_cc(1, utils.r.randint(10, 50))


if __name__ == "__main__":
    s.play()
