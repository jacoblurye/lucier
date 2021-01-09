import functools
import asyncio
from typing import Callable, List, NoReturn, Optional, Sequence

import mido


class MidiController:
    def __init__(self, channel: int):
        self.channel = channel
        self.port = None
        self.note_tasks = {}

    def _set_port(self, port: mido.ports.BaseOutput):
        self.port = port

    def reset(self):
        for note, task in self.note_tasks.items():
            task.cancel()
            self.note_off(note)

    def note_off(self, note: int):
        self.port.send(mido.Message("note_off", note=note, channel=self.channel))

    def note_on(self, note: int, velocity: int):
        self.port.send(
            mido.Message("note_on", note=note, velocity=velocity, channel=self.channel)
        )

    def set_cc(self, control: int, value: int):
        self.port.send(
            mido.Message(
                "control_change", control=control, value=value, channel=self.channel
            )
        )

    async def play_note(self, note: int, velocity: int, duration: float):
        if note in self.note_tasks:
            self.note_tasks[note].cancel()
            self.note_off(note)
        self.note_on(note, velocity)
        await asyncio.sleep(duration)
        self.note_off(note)


Generator = Callable[[MidiController, int], NoReturn]


class Sequencer:
    def __init__(self, output_port: str = "IAC Driver Bus 1", bpm=120, tps=100):
        self.bpm = bpm
        self.spt = bpm / 60 / tps
        self.port = mido.open_output(output_port, autoreset=True)
        self.generators: List[Generator] = []
        self.controllers: List[MidiController] = []
        self.tick = 0

    def register(self, controllers: List[MidiController]):
        self.controllers.extend(controllers)

        for ctrl in controllers:
            ctrl._set_port(self.port)

        def decorator(generator):
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
        if self.generators == []:
            raise Exception("sequencer has no generators")

        try:
            asyncio.run(self._loop())
        except KeyboardInterrupt:
            for controller in self.controllers:
                controller.reset()
