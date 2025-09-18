# font-fitter-engine

An engine to help you fit fonts algorithmically.
How to best fit glyphs on a space is a complicated problem to solve. Font designers spend a lot of their time adjusting whitespace in order to keep the font cohesive.

## Quick start

```
uv run font-fitter-engine run './src/font_fitter_engine/examples'
```

## Technical details

Our Font fitter engine consists of 5 main parts

- Main runner
  This contains the high level apis of our engine. `run()` to fit a font based on set configuration and `validate()` to analyze the behaviour of an algorithm.

  - Loader: loads font files. TTF Loader.
  - Searcher: Searchs amongst the space. Step Searcher.
    - Transforms: Transforms the loaded fonts. SDF transform.
  - Algos: The core algorithm on how to space fonts. Density.

Having our dependencies injected at run time allows the engine to be very flexible. This means new algorithms can be easily added without managing the other boiler plate like loading/transforming.

## Test coverage

Tests is lacking

## License

This project is licensed under the terms of the MIT license.
