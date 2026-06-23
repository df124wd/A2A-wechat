# Correlation ID and reply-to

Messages should support both a `correlation_id` for grouping a request, delegation, tool call, result, error, or refusal into one traceable chain, and a `reply_to` reference for identifying the message being directly answered. This keeps the protocol useful for both chain-level inspection and precise message-level navigation.
