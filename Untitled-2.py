from twitter import *

t = Twitter(auth=OAuth("bl6KLAAAAAAACIKFAAABiPCPgQU", "aF11fjyzlPPiOzxfYzm4vvZoalkpb1AE", "3rJOl1ODzm9yZy63FACdg", "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"))

t.search.tweets(q="#pycon")