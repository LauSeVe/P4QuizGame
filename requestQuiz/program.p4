#include <core.p4>
#include <xsa.p4>

const bit<16> TYPE_QUIZREQUEST = 0x1111;

header ethernet_t {
    bit<48> dstAddr;      // Destination MAC address.
    bit<48> srcAddr;      // Source MAC address.
    bit<16> etherType;    // Ethernet type
}

header quizrequest_t {
    bit<4> session;
    bit<2> type;
    bit<2> lvl;
    bit<160> question;
    bit<160> answer1;
    bit<160> answer2;
    bit<160> answer3;
}

struct headers {
    ethernet_t ethernet;
    quizrequest_t quizrequest;
}

struct smartnic_metadata {
    bit<64> timestamp_ns;    // 64b timestamp (nanoseconds). Set when the packet arrives.
    bit<16> pid;             // 16b packet id for platform (READ ONLY - DO NOT EDIT).
    bit<3>  ingress_port;    // 3b ingress port (0:CMAC0, 1:CMAC1, 2:HOST0, 3:HOST1).
    bit<3>  egress_port;     // 3b egress port (0:CMAC0, 1:CMAC1, 2:HOST0, 3:HOST1).
    bit<1>  truncate_enable; // Reserved (tied to 0).
    bit<16> truncate_length; // Reserved (tied to 0).
    bit<1>  rss_enable;      // Reserved (tied to 0).
    bit<12> rss_entropy;     // Reserved (tied to 0).
    bit<4>  drop_reason;     // Reserved (tied to 0).
    bit<32> scratch;         // Reserved (tied to 0).
}

parser ParserImpl(packet_in packet,
                   out headers hdr,
                   inout smartnic_metadata sn_meta,
                   inout standard_metadata_t smeta) {
    state start {
        transition parse_ethernet;
    }

    // Parse Ethernet header.
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_QUIZREQUEST: parse_quizrequest; 
            default: accept;
        }
    }
    state parse_quizrequest {
        packet.extract(hdr.quizrequest);
        transition accept;
    }
}

control MatchActionImpl(inout headers hdr,
                         inout smartnic_metadata sn_meta,
                         inout standard_metadata_t smeta) {

    action dropPacket(){
        smeta.drop = 1;
    }

    action lvl1Forward(bit<160> question, bit<160> answer1, bit<160> answer2, bit<160> answer3){ 
        hdr.quizrequest.question = question;
        hdr.quizrequest.answer1 = answer1;
        hdr.quizrequest.answer2 = answer2;
        hdr.quizrequest.answer3 = answer3;
    }

    table lvl1 {
        key = {hdr.quizrequest.session : exact;}
        actions = { 
            lvl1Forward;
            dropPacket;
        }
        size = 1024; 
        default_action = dropPacket; 
    }

    action lvl2Forward(bit<160> question, bit<160> answer1, bit<160> answer2, bit<160> answer3){ 
        hdr.quizrequest.question = question;
        hdr.quizrequest.answer1 = answer1;
        hdr.quizrequest.answer2 = answer2;
        hdr.quizrequest.answer3 = answer3;
    }

    table lvl2 {
        key = {hdr.quizrequest.session : exact;}
        actions = { 
            lvl2Forward;
            dropPacket;
        }
        size = 1024; 
        default_action = dropPacket; 
    }

    action lvl3Forward(bit<160> question, bit<160> answer1, bit<160> answer2, bit<160> answer3){ 
        hdr.quizrequest.question = question;
        hdr.quizrequest.answer1 = answer1;
        hdr.quizrequest.answer2 = answer2;
        hdr.quizrequest.answer3 = answer3;
    }

    table lvl3 {
        key = {hdr.quizrequest.session : exact;}
        actions = { 
            lvl3Forward;
            dropPacket;
        }
        size = 1024; 
        default_action = dropPacket; 
    }

    action lvl4Forward(bit<160> question, bit<160> answer1, bit<160> answer2, bit<160> answer3){ 
        hdr.quizrequest.question = question;
        hdr.quizrequest.answer1 = answer1;
        hdr.quizrequest.answer2 = answer2;
        hdr.quizrequest.answer3 = answer3;
    }

    table lvl4 {
        key = {hdr.quizrequest.session : exact;}
        actions = { 
            lvl4Forward;
            dropPacket;
        }
        size = 1024; 
        default_action = dropPacket; 
    }


    apply {
        if (hdr.ethernet.isValid()){
            if (hdr.quizrequest.isValid()){
                if (hdr.quizrequest.type == 1){
                    hdr.quizrequest.type = 2;
                    if(hdr.quizrequest.lvl == 0){
                        lvl1.apply();
                    }
                    else if(hdr.quizrequest.lvl == 1){
                        lvl2.apply();
                    }
                    else if(hdr.quizrequest.lvl == 2){
                        lvl3.apply();
                    }
                    else if(hdr.quizrequest.lvl == 3){
                        lvl4.apply();
                    }
                    else{
                        dropPacket();
                    }
                }
                else{
                    dropPacket();
                }
            }
            else {
               dropPacket();
            }
        }
        else {
           dropPacket();
        }
    }

}

control DeparserImpl(packet_out packet,
                      in headers hdr,
                      inout smartnic_metadata sn_meta,
                      inout standard_metadata_t smeta) {
    apply {
        packet.emit(hdr.ethernet);  // Emit the Ethernet header.
        packet.emit(hdr.quizrequest);  // Emit the quizrequest header.
    }
}

XilinxPipeline(
    ParserImpl(), 
    MatchActionImpl(), 
    DeparserImpl()
) main;
