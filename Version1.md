# Lightshow Version 1

## Core Component
Contains classes Song, Effect, Show

- Song is an abstract class representing a song. Its derived classes can be songs from mp3's, spotify, etc.
- Effect is an abstract class representing something that the lights can do.
    - Its derived classes include sliders, alternators, pulses, etc
    - Contains the start count of the Effect and length (in counts) of the Effect
    - The derived classes also contain all the settings
- Show is a class that contains a Song, an array of Effects, and all the information for playing them together
- Effects, shows, and songs can be serialized and desearialized, allowing saving and reopening of a show file

## Renderer Compenent
Renders a Show object to a file based on the light setup
- The rendered file contains a list of times at which any lights change, followed by a list of the lights that change at that time and what they change to

## GUI Component
Displays and allows for the editing of a show.
Provides a render button that uses the renderer component to generate a rendered show

## Playback Component
Reads a rendered Show from a file and sends command to a LightShowOutput object

## LightShowOutput Component
- Contains two objects
    - One that controls a real arrangement of LED strips
    - One that controls a simulated arrangement of LED strips on the computer screen

## Other Notes
- Version one only creates shows for one strand. Addtional strands will just run a duplicate of the show
- Only works with locally stored mp3's

## Planned Effects
- Add a Sequence object, which represents a sequence of Shows
- Test having the playback component read a Show object directly instead of a rendered version of it and use whichever method has best performance
- Ability to work with single-color LED strips and strips that are don't have independently controllable pixels (are all the same color)
- Add support for RGBW (W is for white) Neopixels
- In the renderer, we should be able to specify whether to start from the beginning, middle, or end of the strand for index 0
- Support for streaming songs from spotify

## Render File Protocol
(Protocol Version)

(Number of LEDs in strand)

Each count that contains at least one change:
(Timestamp) (r0 g0 b0) (r1 g1 b1) ... (rn gn bn) newline
(EOF Indicator)