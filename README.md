# CAPTCHA breaking
The game uses a CAPTCHA system + windows generated input detection to filter out botting activities.
Screenshot data are labelled, post-processed to generate training data set. These are then trained to create a model
that will send keystrokes.
# Automate actions
Again the game has capabilities to identify whether the input was generated using keyboard/mouse or windows (Win API).
Leonardo microcontroller is used alongside to generate input which sends signal to your PC as a same signal as the keyboard/mouse input.
Screencapture was used to localize the character to perform activities that are optimized to maximize returns, such as in-game currency and level.
# Integrate Above parts
CAPTCHA breaker and action automator are integrated into single python files to be ran together forever until the PC shuts down.
Pause function is incorporated to halt the software.
