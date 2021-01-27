Sequence MIDI messages using a [`Flask`](https://github.com/pallets/flask)-style interface.

### Installation

```
pip install lucier
```

### Usage

`lucier` is built around three core constructs:
* **`Sequencer`s**: objects that broadcast time data via `tick`s.
* **`MidiController`s**: objects that send MIDI messages on a given MIDI channel.
* **MIDI generator functions**: `async` functions that subscribe to time from a `Sequencer` and take a `MidiController` and `tick` as their arguments, triggering MIDI events for the current `tick` using the given `MIDIController`.

Here's a basic example of these three constructs working together to play alternating notes on MIDI channels 1 and 2.

```python
from lucier import Sequencer, MidiController, utils

s = Sequencer()

@s.register([MidiController(0)])
async def low_melody(ctrl: MidiController, tick: int):
    """Trigger a .5-second-long C4 note every 50 ticks."""
    if utils.every_n_ticks(50, tick):
        await ctrl.play_note(60, 60, .5)

@s.register([MidiController(1)])
async def high_melody(ctrl: MidiController, tick: int):
    """Trigger a .5-second-long C5 note every 50 ticks, starting after 25 ticks."""
    if utils.every_n_ticks(50, tick, offset=25):
        await ctrl.play_note(72, 60, .5)

# Run the sequencer
s.play()
```
