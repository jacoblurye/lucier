Sequence MIDI messages using a [`Flask`](https://github.com/pallets/flask)-style interface. Very much a work-in-progress.

### Installation

[todo]

### Usage

```python
from lucier import Sequencer, MidiController, utils

s = Sequencer()

@s.register([MidiController(0)])
async def low_melody(ctrl, tick):
    if utils.every_n_ticks(50, tick):
        await ctrl.play_note(60, 60, .5)

@s.register([MidiController(1)])
async def high_melody(ctrl, tick):
    if utils.every_n_ticks(50, tick, offset=25):
        await ctrl.play_note(72, 60, .5)

s.play()
```
