#include <core.p4>
#include <xsa.p4>


header ethernet_t {
    bit<48> dstAddr;      // Destination MAC address.
    bit<48> srcAddr;      // Source MAC address.
    bit<16> etherType;    // Ethernet type
}

header quiz0_t {
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
    quiz0_t quiz0;
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
            default: accept;
        }
    }
    state parse_quiz0 {
        packet.extract(hdr.quiz0);
        transition accept;
    }
}

control MatchActionImpl(inout headers hdr,
                         inout smartnic_metadata sn_meta,
                         inout standard_metadata_t smeta) {

    action dropPacket(){
        smeta.drop = 1;
    }

    action lvl1Forward(bit<160> question){
        hdr.quiz0.question = question;
    }

    table lvl1 {
        key = {hdr.quiz0.session : exact;}
        actions = { 
            lvl1Forward;
            dropPacket;
        }
        size = 1024; 
        default_action = dropPacket; 
    }


    apply {
        if (hdr.ethernet.isValid()){
            if (hdr.quiz0.isValid()){
                if (hdr.quiz0.lvl == 0){
                    lvl1.apply();
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
        packet.emit(hdr.quiz0);
    }
}

XilinxPipeline(
    ParserImpl(), 
    MatchActionImpl(), 
    DeparserImpl()
) main;
