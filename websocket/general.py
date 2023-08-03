def construct(message_type, data):
    """Constructs message with a predetermined form"""
    return {
        "type": message_type,
        "data": data
    }
