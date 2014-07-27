import pygame
import sys
import random

class MarkovChainMid(object):
    def __init__(self, listOfChunkTuples = None):
        self.corpus = listOfChunkTuples
        self.chain = self.setChain()
    def setChain(self):
        chain = {}
        
        mx = len(self.corpus)-1
        for i,x in enumerate(self.corpus):
            if i == mx :
                pass
            else:
                try:
                    chain[x].append(self.corpus[i+1])
                except KeyError as e:
                    chain[x] =[self.corpus[i+1]]

        try:
            chain[mx].append(self.corpus[-1])
        except KeyError as e:
            chain[mx] = [self.corpus[-1]]
        return(chain)

    def printSth(self,maxItems = 20):
        res = []
        t = self.corpus[0]
        res += t 
        for i in range(0,maxItems):
            try:
                tmp = random.choice(self.chain[t])
                res += tmp
                t= tmp
            except KeyError as e:
                return(res)
        return(res)

def playMidi(midifile):
    clock = pygame.time.Clock()
    pygame.mixer.music.load(midifile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)

def takeAByte(midifile):
    with open(midifile, "rb") as f:
        byte = f.read(1)
        while byte != "":
            yield(byte)
            byte = f.read(1)
        yield(byte)


def chunkIt(listofbytes,chunksize):
    return zip(*[iter(listofbytes)]*chunksize)




def main():
    midifile = sys.argv[1]
    freq = 44100
    bitsize = -16 
    channels = 2
    buffer = 1024 
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(0.8)
    ###
    midibytes =[]
    for b in takeAByte(midifile):
        midibytes.append(b)

    #print(midibytes[0:3])
    chunk = chunkIt(midibytes,8)
    mcm = MarkovChainMid(chunk)
    #print(mcm.chain)
    res = (mcm.printSth(1000))
    with open(midifile+".t", 'wb') as out:
        out.write("".join(res))
    
    ### play
    try:
        playMidi(midifile+".t")
    except KeyboardInterrupt:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
if __name__ == "__main__":
    main()
