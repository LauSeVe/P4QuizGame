#include <core.p4>
#include <xsa.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_IPV6 = 0x86dd;

header ethernet_t {
    bit<48> dstAddr;      // Destination MAC address.
    bit<48> srcAddr;      // Source MAC address.
    bit<16> etherType;    // Ethernet type
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    bit<32>   srcAddr;
    bit<32>   dstAddr;
}

header ipv6_t {
    bit<4> version;
    bit<8> traffic_class;
    bit<20> flow_label;
    bit<16> payload_len;
    bit<8> next_hdr;
    bit<8> hop_limit;
    bit<128> src_addr;
    bit<128> dst_addr;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    ipv6_t ipv6;
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
            TYPE_IPV4: parse_ipv4;
            TYPE_IPV6: parse_ipv6;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }
    state parse_ipv6 {
        packet.extract(hdr.ipv6);
        transition accept;
    }
}

control MatchActionImpl(inout headers hdr,
                         inout smartnic_metadata sn_meta,
                         inout standard_metadata_t smeta) {

    action dropPacket(){
        smeta.drop = 1;
    }

    table etherTable {
        key = {hdr.ethernet.etherType : exact; }
        actions = { dropPacket ; NoAction; }
        size = 1024;
        default_action = dropPacket;
    }

    table ipv4_filter{
        key = { hdr.ipv4.srcAddr: exact;}
        actions = {dropPacket ; NoAction;}
        size = 1024;
        default_action = NoAction;
    }

    table ipv6_filter{
        key = { hdr.ipv6.src_addr: exact;}
        actions = {dropPacket ; NoAction;}
        size = 1024;
        default_action = NoAction;
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
