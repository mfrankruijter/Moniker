import re, codecs, json, time, io, urllib2

class Config():
    def __init__(self, configFile=None):
        try:
            with codecs.open(configFile, encoding="utf-8-sig", mode="r") as configFile:
                self.__dict__ = json.load(configFile, encoding="utf-8")
        except:
            self.inputs = {}
            self.outputs = {}
            self.fetchFrequency = 10
            self.fetchInputs = {}

class Handler():
    def __init__(self, config):
        self.outputs = []
        self.monikers = config.inputs
        self.fetchFrequency = config.fetchFrequency
        self.fetchInputs = config.fetchInputs

        for outputFile in config.outputs:
            self.outputs.append(
                {
                    'file': config.outputs[outputFile]['file'],
                    'monikers': re.findall('{([A-z0-9_-]+)}', config.outputs[outputFile]['text']),
                    'text': config.outputs[outputFile]['text']
                }
            )
        
    def subscribe(self):
        buffers = {}
        content = {}
        fetchContent = {}
        for moniker in self.monikers.keys():
            buffers[moniker] = io.open(self.monikers[moniker], 'r')
            content[moniker] = ''
            fetchContent[moniker] = ''
        changed = False
        changedKeys = []
        count = 1
        while True:
            if count == self.fetchFrequency:
                count = 0
                for endpoint in self.fetchInputs:
                    webStream = urllib2.urlopen(self.fetchInputs[endpoint])
                    writeStream = io.open(self.monikers[endpoint], 'w+')
                    writeStream.write(webStream.read().decode('utf-8'))
                    writeStream.close()
            changedKeys = []
            for moniker in buffers.keys():
                buffers[moniker].seek(0)
                newContent = buffers[moniker].read()
                if content[moniker] != newContent:
                    changed = True
                    changedKeys.append(moniker)
                    content[moniker] = newContent

            if changed:
                for outputFile in self.outputs:
                    for key in changedKeys:
                        if key in outputFile['monikers']:
                            outputText = outputFile['text']
                            for moniker in outputFile['monikers']:
                                outputText = outputText.replace('{' + moniker + '}', content[moniker])

                            writeStream = io.open(outputFile['file'], 'w+')
                            writeStream.write(outputText)
                            writeStream.close()
                            break
            changed = False
            count+=1
            time.sleep(1)
