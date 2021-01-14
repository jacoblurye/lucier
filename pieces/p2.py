from lucier import Sequencer, MidiController, utils

scale = utils.major_scale(55)
lead_chords = [
    utils.random_iter(
        [
            scale[shift],
            scale[(shift + 2) % 7],
            scale[(shift + 3) % 7],
            scale[(shift + 5) % 7],
        ]
    )
    for shift in [0, 2, 4, 6]
]
bass_chords = [utils.random_iter([scale[(shift + 5) % 7]]) for shift in [0, 2, 4, 6]]
s = Sequencer(tps=100)


def get_note(tick: int, chords=lead_chords):
    if tick % 400 < 100:
        return next(chords[0])
    if tick % 400 < 200:
        return next(chords[1])
    if tick % 400 < 300:
        return next(chords[2])
    if tick % 400 < 400:
        return next(chords[3])


up = utils.maybe_8va(4)
rare_up = utils.maybe_8va(10)
mult = utils.random_iter([1, 2])


@s.register([MidiController(c) for c in [0, 1, 2, 11, 12, 13]])
async def harps(ctrl: MidiController, tick: int):
    ratio = utils.incperc(tick, 0.001)
    if (
        utils.every_n_ticks(75, tick + utils.r.randint(-20, 20))
        and utils.coin_flip(0.9 * ratio)
    ) or utils.coin_flip(0.04):
        await ctrl.play_note(
            get_note(tick) + 12 + next(up) + next(up) + next(rare_up) - next(up),
            utils.sine(tick, 80, 100 + 26 * ratio, 75) + utils.r.randint(-5, 5),
            1,
        )


@s.register([MidiController(c) for c in range(9, 11)])
async def synth(ctrl: MidiController, tick: int):

    if utils.every_n_ticks(100, tick):
        await ctrl.play_note(
            get_note(tick, bass_chords) - 24, utils.r.randint(60, 90), 3
        )

    if utils.every_n_ticks(100, tick + utils.r.randint(15, 65)):
        await ctrl.play_note(get_note(tick), utils.r.randint(20, 55), 3)

    if tick % 50:
        ctrl.set_cc(10, utils.r.randint(10, 117))

    ctrl.set_cc(1, utils.sine(tick, 0, 5, 100))

    if utils.every_n_ticks(99, tick):
        ctrl.reset()


@s.register([MidiController(c) for c in range(3, 9)])
async def strings(ctrl: MidiController, tick: int):
    ratio = utils.incperc(tick, 0.001)
    period = 100 + (ctrl.channel - 3) // 3 * 50
    ctrl.set_cc(1, utils.sine(tick, 70 + 15 * ratio, 90 + 36 * ratio, period, 50))
    ctrl.set_cc(11, utils.sine(tick, 10 + 50 * ratio, 90 + 36 * ratio, period, 50))

    random_play = utils.coin_flip(0.05 + 0.05 * ratio)
    if (
        utils.every_n_ticks(100 + utils.r.randint(40, 60), tick)
        and utils.coin_flip(0.5)
    ) or random_play:
        await ctrl.play_note(
            get_note(tick) + next(up) + next(up) + next(rare_up),
            50,
            0.75 + utils.r.randint(-1, 2),
        )


if __name__ == "__main__":
    s.play()