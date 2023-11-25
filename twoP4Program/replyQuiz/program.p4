#include <core.p4>
#include <xsa.p4>

const bit<16> TYPE_QUIZREPLY = 0x2222;

header ethernet_t {
    bit<48> dstAddr;      // Destination MAC address.
    bit<48> srcAddr;      // Source MAC address.
    bit<16> etherType;    // Ethernet type
}

header quizreply_t {
    bit<4> session;
    bit<2> type;
    bit<2> correct;
    bit<160> question;
    bit<160> user_answer;
}

struct headers {
    ethernet_t ethernet;
    quizreply_t quizreply;
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
            TYPE_QUIZREPLY: parse_quizreply; 
            default: accept;
        }
    }
    state parse_quizreply {
        packet.extract(hdr.quizreply);
        transition accept;
    }
}

control MatchActionImpl(inout headers hdr,
                         inout smartnic_metadata sn_meta,
                         inout standard_metadata_t smeta) {

    action dropPacket(){
        smeta.drop = 1;
    }

    action forwardPacket(bit<160> answer){ 
        hdr.quizreply.user_answer = answer;
    }

    table comprobation {
        key = {hdr.quizreply.question : exact;}
        actions = { 
            forwardPacket;
            dropPacket;
        }
        size = 1024; 
        default_action = dropPacket; 
    }


    apply {
        bit<160> user_answer_tmp = hdr.quizreply.user_answer;
        if (hdr.ethernet.isValid()){
            if (hdr.quizreply.isValid()){
                if (hdr.quizreply.type == 2){
                    hdr.quizreply.type = 3;
                    comprobation.apply();
                    if (user_answer_tmp == hdr.quizreply.user_answer){
                    hdr.quizreply.correct = 0x1;
                    }
                    else {
                    hdr.quizreply.correct = 0x2;
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
        packet.emit(hdr.quizreply);  // Emit the quizreply header.
    }
}

XilinxPipeline(
    ParserImpl(), 
    MatchActionImpl(), 
    DeparserImpl()
) main;
