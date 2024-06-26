# PlatformIO + STM8-DCE
[![PlatformIO CI](https://github.com/maxgerhardt/pio-stm8-dce/actions/workflows/build.yml/badge.svg)](https://github.com/maxgerhardt/pio-stm8-dce/actions/workflows/build.yml) <a href="https://github.com/maxgerhardt/pio-stm8-dce/commits/master"><img src="https://img.shields.io/github/last-commit/maxgerhardt/pio-stm8-dce.svg" alt="last commit"> <a href="https://github.com/maxgerhardt/pio-stm8-dce/issues"><img src="https://img.shields.io/github/issues/maxgerhardt/pio-stm8-dce.svg" alt="open issues"> [![Pull Requests](https://img.shields.io/github/issues-search/maxgerhardt/pio-stm8-dce?label=merged%20PRs&query=is%3Apr+is%3Aclosed+is%3Amerged)](https://img.shields.io/github/issues-search/maxgerhardt/pio-stm8-dce?label=merged%20PRs&query=is%3Apr+is%3Aclosed+is%3Amerged)

See project https://github.com/CTXz/STM8-DCE for main information.

This is an example project that integrates the STM8 Dead Code Eliminator into the PlatformIO build process.

Shortly before PlatformIO wants to link the firmware from the generated `.rel` files, the extra script runs all generated assembly files through the dead code optimizer and then regenerates the `.rel` (and `.lst` and `.sym`) files based of them.

In even the simplest [GPIO blink demo](https://github.com/platformio/platform-ststm8/tree/develop/examples/spl-blink), this optimization makes the project go from

```
RAM:   [          ]   0.0% (used 0 bytes from 1024 bytes)
Flash: [=         ]   8.0% (used 655 bytes from 8192 bytes)
```

to

```
RAM:   [          ]   0.0% (used 0 bytes from 1024 bytes)
Flash: [=         ]   6.6% (used 540 bytes from 8192 bytes)
```

it might have an even bigger impact in larger projects that uses more parts of the SPL.

Note: This is only tested against `framework = spl`. The `framework = arduino` framework uses SDCC 3.x instead of 4.x, which the STM8-DCE tool might fail against.