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
            self.customInputs = {}

class Handler():
    def __init__(self, config, customHandlers={}):
        self.outputs = []
        self.monikers = config.inputs
        self.fetchFrequency = config.fetchFrequency
        self.fetchInputs = config.fetchInputs
        self.customInputs = config.customInputs
        self.customHandlers = customHandlers

        for outputFile in config.outputs:
            if 'onEmpty' in config.outputs[outputFile]:
                self.outputs.append(
                    {
                        'file': config.outputs[outputFile]['file'],
                        'monikers': re.findall('{([A-z0-9_\\.-]+)}', config.outputs[outputFile]['text']),
                        'text': config.outputs[outputFile]['text'],
                        'onEmpty': config.outputs[outputFile]['onEmpty']
                    }
                )
            else:
                self.outputs.append(
                    {
                        'file': config.outputs[outputFile]['file'],
                        'monikers': re.findall('{([A-z0-9_\\.-]+)}', config.outputs[outputFile]['text']),
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
                    webStream.close()
            changedKeys = []
            for moniker in buffers.keys():
                buffers[moniker].seek(0)
                newContent = buffers[moniker].read()
                if content[moniker] != newContent:
                    changed = True
                    changedKeys.append(moniker)
                    content[moniker] = newContent

            for customKey in self.customInputs:
                customResult = self.customHandlers[self.customInputs[customKey]['type']].handle(customKey, self.customInputs[customKey]['config'])
                for customFieldKey in customResult:
                    try:
                        if content[customFieldKey] != customResult:
                            changed = True
                            changedKeys.append(customFieldKey)
                            content[customFieldKey] = customResult[customFieldKey]
                    except:
                        changed = True
                        changedKeys.append(customFieldKey)
                        content[customFieldKey] = customResult[customFieldKey]

            if changed:
                for outputFile in self.outputs:
                    if 'onEmpty' in outputFile:
                        if content[outputFile['onEmpty']['field']] == '':
                            writeStream = io.open(outputFile['file'], 'w+')
                            writeStream.write(outputFile['onEmpty']['result'])
                            writeStream.close()
                            continue

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
