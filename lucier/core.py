import functools
import asyncio
from typing import Callable, List, NoReturn, Optional, Sequence

import mido


class MidiController:
    """Trigger note and other CC parameter events on a particular MIDI channel.

    Use as a standalone or connect to a `Sequencer` instance via the `Sequencer.register` method.

    Args:
        channel: the MIDI channel to send messages on.
    """

    def __init__(self, channel: int):
        self.channel = channel
        self.port = None
        self.note_tasks = {}

    def _set_port(self, port: mido.ports.BaseOutput):
        self.port = port

    def reset(self):
        """Send `note_off` messages for any currently playing notes."""
        for note, task in self.note_tasks.items():
            task.cancel()
            self.note_off(note)

    def note_off(self, note: int):
        """Send a `note_off` MIDI message with the given `note` value."""
        self.port.send(mido.Message("note_off", note=note, channel=self.channel))

    def note_on(self, note: int, velocity: int):
        """Send a `note_on` MIDI message with the given `note` and `velocity` values."""
        self.port.send(
            mido.Message("note_on", note=note, velocity=velocity, channel=self.channel)
        )

    def set_cc(self, control: int, value: int):
        """Send a MIDI message to CC `control` with the given `value`."""
        self.port.send(
            mido.Message(
                "control_change", control=control, value=value, channel=self.channel
            )
        )

    async def play_note(self, note: int, velocity: int, duration: float):
        """Play a `note` at a `velocity` for a `duration` (in seconds)."""
        if note in self.note_tasks:
            self.note_tasks[note].cancel()
            self.note_off(note)
        self.note_on(note, velocity)
        await asyncio.sleep(duration)
        self.note_off(note)


Generator = Callable[[MidiController, int], NoReturn]


class Sequencer:
    """Provide time data to sets of MidiControllers, triggering time-based events.

    Args:
        output_device: the name of the MIDI output device to use.
        tps: ticks per second, how many time events are fired per second.

    Examples:
        >>> s = Sequencer()
        >>> @s.register([MidiController(1), MidiController(2)])
        ... async def music_generator(ctrl, tick):
        ...     ctrl.play_note(60, 60, 1)

    Todos:
        Shift from using ticks per second to configure the sequencer's speed
        to beats per minute and pulses per beat. This allows for configuring speed
        and rhythmic resolution separately, via BPM and PPB respectively.
    """

    def __init__(self, output_device: str = "IAC Driver Bus 1", tps=100):
        self.tps = tps
        self.spt = 1 / tps
        self.port = mido.open_output(output_device, autoreset=True)
        self.generators: List[Generator] = []
        self.controllers: List[MidiController] = []
        self.tick = 1

    def register(self, controllers: List[MidiController]):
        """Decorator for an asynchronous function that takes a `MidiController` and
        the current `tick` as its arguments.

        Every time this `Sequencer` instance's `tick` value increases, it will call
        this function with the updated tick value, once for each `MidiController` in
        the provided list of `controllers`.
        """
        self.controllers.extend(controllers)

        for ctrl in controllers:
            ctrl._set_port(self.port)

        def decorator(generator: Generator):
            @functools.wraps(generator)
            async def wrapped(tick: int):
                for ctrl in controllers:
                    await generator(ctrl, tick)

            self.generators.append(wrapped)

            return wrapped

        return decorator

    async def _loop(self):
        while True:
            for subscriber in self.generators:
                asyncio.create_task(subscriber(self.tick))
                await asyncio.sleep(self.spt)
            self.tick += 1

    def play(self):
        """Run the sequencer, starting from a tick value of 1."""
        if self.generators == []:
            raise Exception("sequencer has no generators")

        try:
            asyncio.run(self._loop())
        except KeyboardInterrupt:
            for controller in self.controllers:
                controller.reset()
            self.tick = 1
