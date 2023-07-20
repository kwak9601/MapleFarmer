Automation tool that performs repetitive tasks to earn exp and in-game currency.
Done in human-like way, is able to break CAPTCHA system.

# CAPTCHA breaking
The game uses a CAPTCHA system + windows generated input detection to filter out botting activities.
Screenshot data are labeled, post-processed to generate a training data set. These are then trained to create a model
that will send keystrokes.
# Automate actions
Again the game has capabilities to identify whether the input was generated using a keyboard/mouse or windows (Win API).
Leonardo microcontroller is used alongside to generate input which sends a signal to your PC as the same signal as the keyboard/mouse input.
Screen capture was used to localize the character to perform activities that are optimized to maximize returns, such as in-game currency and level.
# Integration
After writing the sketch file to the microcontroller, 
CAPTCHA breaker and action Automator are integrated into single Python files to run together forever until the PC shuts down.
The pause function is incorporated to halt the software.
