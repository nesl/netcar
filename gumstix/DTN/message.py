"""
  Copyright (c) 2003 The Regents of the University of California.
  All rights reserved.
 
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above
     copyright notice, this list of conditions and the following
     disclaimer in the documentation and/or other materials provided
     with the distribution.
  3. Neither the name of the University of California nor the names of
     its contributors may be used to endorse or promote products derived 
     from this software without specific prior written permission.
 
  THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS
  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
  USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
  SUCH DAMAGE.


  @author Thomas Schmid <thomas.schmid@ucla.edu>
"""

import struct
import logging

class Message:
    """
        This is the base class for messages. It defines some
        functions and valiables every message should have.
    """

    def __init__(self, msgType=-1, content="", msg=None):
        self._log = logging.getLogger("Message")
        self._log.setLevel(logging.DEBUG)

        if msgType > 255:
            raise Error("msgType too large")
        if msgType > 0:
            self._msgType = msgType
            self._content = content
        elif msg != None:
            self.decode(msg)

    def encode(self):
        return struct.pack("!BH%ds"%(len(self._content),), self._msgType, len(self._content), self._content)

    def decode(self, msg):
        (self._msgType, length) = struct.unpack("!BH", msg[0:struct.calcsize("!BH")])
        self._log.debug("len: %d, calcsize: %d, msglen: %d"%(length, struct.calcsize("!BH"), len(msg)))
        (self._content,) = struct.unpack("%ds"%(length,), msg[struct.calcsize("!BH"):])

    def __str__(self):
        return "type: %d, content: %s"%(self._msgType, self._content)
