from scapy.all import Packet, BitField, StrFixedLenField

TYPE_QUIZ_REQUEST=0x1111
TYPE_QUIZ_REPLY=0x2222

class QuizHeaderRequest(Packet):
    name = "QuizHeaderRequest"
    fields_desc = [
        BitField("session", 0, 4),
        BitField("type", 0, 2),
        BitField("lvl", 0, 2),
        StrFixedLenField("question", b"\x00" * 20, length=20),
        StrFixedLenField("answer1", b"\x00" * 20, length=20),
        StrFixedLenField("answer2", b"\x00" * 20, length=20),
        StrFixedLenField("answer3", b"\x00" * 20, length=20),
    ]

class QuizHeaderReply(Packet):
    name = "QuizHeaderReply"
    fields_desc = [
        BitField("session", 0, 4),
        BitField("type", 0, 2),
        BitField("lvl", 0, 2),
        StrFixedLenField("question", b"\x00" * 20, length=20),
        StrFixedLenField("user_answer", b"\x00" * 20, length=20),
    ]