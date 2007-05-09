class Message:
    """
        This is the base class for messages. It defines some
        functions and valiables every message should have.
    """
    def __init__(self, msgType, content):
        if msgType > 255:
            raise Error("msgType too large")
        self._msgType = msgType
        self._content = content

    def __str__(self):
        return "%0c%s"%(self._msgType, self._content)
