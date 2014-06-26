from trading.strategy import Test, RISK, OIL, VIX
from datetime import timedelta

DELTA = 15
FREQUENCY = timedelta(minutes=DELTA)

ACTIVE = ['Test']
STRATEGIES = dict((cls,globals()[cls]()) for cls in ACTIVE)