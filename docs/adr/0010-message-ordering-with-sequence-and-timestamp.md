# Message ordering with sequence and timestamp

Messages should carry both a sequence number for stable trace ordering and a timestamp for real-time observation. This avoids ambiguous ordering in asynchronous runs while keeping causality modeling lighter than a full parent graph in the first protocol version.
