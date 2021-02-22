[![Buy me a coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoff.ee/pulsebear)

# Moniker - Active file manipulator

This package contains a standalone script which allows the user to configure 
different inputs, manipulate the data and send it to an output file. This 
script can for example help with setting up dynamic files which can be read by 
OBS.

## Installation

In order to run this script, you need to have Python 2.7 installed the correct
version can be found here: https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi
To use the script without changing any code, Python should be installed to: 
`C:\Python27` (the same as for the Streamlabs Chatbot).

If it is installed elsewhere, open the `execute_moniker_background.bat` 
and `execute_moniker_foreground.bat` files in a text editor and change the 
location in those files.

Once Python in installed go to 
(the latest release)[https://github.com/mfrankruijter/Moniker/releases/latest]
and download the ZIP file by clicking on `Source code (zip)`. Unpack this ZIP 
file to the desired location.

## Configuration
The configuration file is located at `config/monikers.json`. 

### inputs
In the `inputs` node, a moniker key can be connected to a filename. This will 
swap out the moniker in the output, with the content of the input file.
The inputs can have an unlimited amount of entries

For example:
```json
{
    "inputs": {
        "input-file": "example-files\\input-file.txt"
    }
}
```

Will create an `{input-file}` moniker, which contains the contents of the file 
`example-files\input-file.txt`. The input file should always exist. The path 
can be an absolute path (full path) or a relative path (relative to the root of
the script).

### fetchInputs
Inputs can also be configured to listen to an endpoint on the web.
This can be done through the `fetchInputs` node. An entry in the `fetchInputs` 
node should have a key which is also present in the `inputs` node. This will 
become the file where the contents of the web endpoint is being written to.

The fetchInputs can have an unlimited amount of entries as long as their key
exists in the `inputs` node.

In the following example the contents of the endpoint are being written to 
`example-files\input-file.txt` and can then be used as a moniker as well:
```json
{
    "fetchInputs": {
        "input-file": "https://pastebin.com/raw/LfNbBpEm"
    },
    "inputs": {
        "input-file": "example-files\\input-file.txt"
    }
}
```

### fetchFrequency
The `fetchFrequency` can be configured to determine the polling rate of any URL 
being called. Every increment is one second. So the default of `10` will result 
in one poll of the endpoint every 10 seconds. This can only be defined once.

```json
{
    "fetchFrequency": 10
}
```

### outputs
In the `outputs` node you can configure where the files are being written to and
how they are contextualized. The initial key `someoutput` (of the example below)
has no internal value, so it is purely used as a placeholder for organizing the
configuration.

In the `file` node the output file can be set. This can be an absolute path 
(full path) or a relative path (relative to the root of the script). The output
file doesn't have to exist, but the directory should be created before running 
the script.

The `text` node contains the output that is being transmitted to the output 
file. The text can be modified with the monikers (from the `inputs`) by adding
their keys between curly braces. Any combination of monikers can be used in 
the output. 

The outputs can have an unlimited amount of entries.

```json
{
    "outputs": {
        "someoutput": {
            "file": "example-files\\output-file.txt",
            "text": "PulseBear has written {input-file} scripts today"
        }
    }
}
```

## Running the script

To run the script in the foreground (seeing a terminal window), double click on
the `execute_moniker_foreground.bat` file. To run it in the background, use the
`execute_moniker_background.bat` file.

When the file is running in the background, it is located under the `pythonw.exe` 
process in the task manager.

If everything is left as is, the code should run as follows:
- The `input-file.txt` is read.
- The data from `input-file.txt` is written to `output-file.txt` with an 
alternated string `PulseBear has written 0 scripts today`
- After 10 seconds, the `input-file.txt` is updated to `3` and the 
`output-file.txt` is immediatly updated as well:
`PulseBear has written 3 scripts today`

## Feedback

Feedback for this package can be provided through issues, or by creating a pull
request with a fix or improvement.

## MIT License

Copyright (c) Marcel Frankruijter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
