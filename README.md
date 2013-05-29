Initial sketch of a Python API and CLI for Ninja Blocks.

Install with pip:

    $ pip install -e git+https://github.com/theojulienne/pyninja#egg=pyninja
    
Then create a file with your user_access_token (from the Ninja Blocks settings tab -> API -> API Access Token):

    $ echo "TOKENHERE" > ~/ninja_token.txt

Now read and actuate to your heart's content:

    $ pyninja -h                     # shows all available commands
    $ pyninja user info              # information about the authenticated user
    $ pyninja device list            # list of all devices available through the API, note the GUIDs
    $ pyninja device info <guid>     # show info a specific device by GUID

Get information on a specific device by GUID:

    $ pyninja device info 1234BB000000_0_0_1231
    GUID: 1234BB000000_0_0_1231
    Name: Temperature
    Type: TemperatureNinjaDevice
    Temperature: 24.3 C
    
You can actuate any device by providing the GUID and the value:
    
    $ pyninja device actuate 1234BB000000_0_0_1234 00FF00
    
There is also bonus CSS3 colour support for any RGB LED (including the eyes):
    
    $ pyninja device actuate 1234BB000000_0_0_1234 purple
    ...
    $ pyninja device info 1234BB000000_0_0_1234
    GUID: 1234BB000000_0_0_1234
    Name: Nina's Eyes
    Type: RGBLEDNinjaDevice
    Color: #800080

