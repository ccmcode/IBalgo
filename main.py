'''
Created on Dec 31, 2013

@author: Colin
'''
from trading.trader import BlindTrader, MarketTrader
from trading import STRATEGIES
from prtf import Portfolio
from optparse import OptionParser
from datetime import date
import logging

log = logging.getLogger(__name__)

RUNNING = True
TODAY = date.today().strftime("%Y%m%d")

help = {'run':  'starts each strategy, pass a comma separated list of strategy names',
        'kill': 'kill each strategy, pass a comma separated list of strategy names',
        'list': 'lists all strategies running',
        'prtf': 'call a function in the prtf class',
        'quit': 'ends the program'}

def parseArgs():
    parser = OptionParser()
    parser.add_option("-c", "--cob", dest="cob", default=TODAY)
    parser.add_option("-s", "--strats", dest="names", default=','.join([n for n in STRATEGIES.keys()]))
    options, args = parser.parse_args()
    return options.cob, options.names
    
def main():
    cob, names = parseArgs()
    cob = TODAY #backtesting not implemented
    strats = [STRATEGIES[n] for n in ",".split(names)]
    prtf = Portfolio(cob)
    
    
    trader = BlindTrader(strats)
    trader.start()
    trader.join()
    trader = MarketTrader()
    trader.start()    
    
    while RUNNING:
        try:
            cmd = raw_input("Type 'help' for a list of commands \nPlease enter a command: ")
            
            if cmd == 'help':
                for k,v in help.iteritems():
                    print k + ' - ' + v
            elif cmd == 'quit':
                [s.terminate() for s in STRATEGIES if s.is_alive()]
                RUNNING = False
            elif cmd == 'run':
                [s.start() for s in strats]
            elif cmd == 'kill':
                if trader: trader.terminate()
                [s.terminate() for s in STRATEGIES if s.is_alive()]
            elif cmd == 'list':
                names = [s.name for s in STRATEGIES if s.is_alive()]
                print names
            else:
                print 'Invalid command'
        except KeyboardInterrupt:
            if trader: trader.terminate()
            [s.terminate() for s in STRATEGIES if s.is_alive()]
            
    log.info("Algo killed")
    
if __name__ == '__main__':
    main()