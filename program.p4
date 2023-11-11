#include <core.p4>
#include <xsa.p4>

const bit<16> TYPE_QUIZ0 = 0x1111;

header ethernet_t {
    bit<48> dstAddr;      // Destination MAC address.
    bit<48> srcAddr;      // Source MAC address.
    bit<16> etherType;    // Ethernet type
}

header quizheader0_t {
    bit<4> session;
    bit<2> type;
    bit<2> lvl;
    byte<20> question;
    byte<20> answer1;
    byte<20> answer2;
    byte<20> answer3;
}

struct headers {
    ethernet_t ethernet;
    quizheader0_t quizheader0;
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
            TYPE_QUIZ0: parse_quiz0;
            default: accept;
        }
    }
    state parse_quiz0 {
        packet.extract(hdr.quizheader0);
        transition accept;
    }
}

control MatchActionImpl(inout headers hdr,
                         inout smartnic_metadata sn_meta,
                         inout standard_metadata_t smeta) {

    action dropPacket(){
        smeta.drop = 1;
    }

    apply {
        if (hdr.ethernet.isValid()){
            etherTable.apply();
            if (hdr.ipv4.isValid()){
                ipv4_filter.apply();
            }
            else if (hdr.ipv6.isValid()){
                ipv6_filter.apply();
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
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv6);
    }
}

XilinxPipeline(
    ParserImpl(), 
    MatchActionImpl(), 
    DeparserImpl()
) main;