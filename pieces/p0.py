from lucier import Sequencer, MidiController, utils

s = Sequencer()

notes = utils.random_iter([47, 38, 31] * 10 + [50])
maybe_8va = utils.random_iter([0] * 5 + [12])


@s.register([MidiController(0), MidiController(1)])
async def slow_boy(ctrl: MidiController, tick: int):
    if utils.coin_flip(0.01):
        note = next(notes) + next(maybe_8va)
        await ctrl.play_note(
            note,
            abs(tick % 7 - tick % 5 - tick % 3 + tick % 2) * 5
            + int((0.05 * tick) % 25),
            30 if note == 31 else 8,
        )

    if tick % 50:
        ctrl.set_cc(10, utils.r.randint(10, 117))
        ctrl.set_cc(74, utils.r.randint(40, 80))

    if tick % 11:
        ctrl.set_cc(1, tick % 2 * 2)


@s.register([MidiController(c) for c in range(2, 16)])
async def fast_boy(ctrl: MidiController, tick: int):
    if utils.coin_flip(0.20):
        await ctrl.play_note(
            next(notes) + 12 + next(maybe_8va),
            abs(tick % 7 - tick % 5 + tick % 3) * 6 + utils.r.randint(0, 60),
            4,
        )


if __name__ == "__main__":
    s.play()
