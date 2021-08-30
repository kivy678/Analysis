typedef struct DeyHeader {
  u1  magic[8];

  u4  dexOffset;
  u4  dexLength;
  u4  depsOffset;
  u4  depsLength;
  u4  optOffset;
  u4  optLength;

  u4  flags;
  u4  checksum;

} DeyHeader;
// 40

def header(mm) :
    magic           = mm[0:8]
    checksum        = struct.unpack('<L', mm[8:0xC])[0]
    sa1             = mm[0xC:0x20]
    file_size       = struct.unpack('<L', mm[0x20:0x24])[0]
    header_size     = struct.unpack('<L', mm[0x24:0x28])[0]
    endian_tag      = struct.unpack('<L', mm[0x28:0x2C])[0]
    link_size       = struct.unpack('<L', mm[0x2C:0x30])[0]
    link_off        = struct.unpack('<L', mm[0x30:0x34])[0]
    map_off         = struct.unpack('<L', mm[0x34:0x38])[0]
    string_ids_size = struct.unpack('<L', mm[0x38:0x3C])[0]
    string_ids_off  = struct.unpack('<L', mm[0x3C:0x40])[0]
    type_ids_size   = struct.unpack('<L', mm[0x40:0x44])[0]
    type_ids_off    = struct.unpack('<L', mm[0x44:0x48])[0]
    proto_ids_size  = struct.unpack('<L', mm[0x48:0x4C])[0]
    proto_ids_off   = struct.unpack('<L', mm[0x4C:0x50])[0]
    field_ids_size  = struct.unpack('<L', mm[0x50:0x54])[0]
    field_ids_off   = struct.unpack('<L', mm[0x54:0x58])[0]
    method_ids_size = struct.unpack('<L', mm[0x58:0x5C])[0]
    method_ids_off  = struct.unpack('<L', mm[0x5C:0x60])[0]
    class_defs_size = struct.unpack('<L', mm[0x60:0x64])[0]
    class_defs_off  = struct.unpack('<L', mm[0x64:0x68])[0]
    data_size       = struct.unpack('<L', mm[0x68:0x6C])[0]
    data_off        = struct.unpack('<L', mm[0x6C:0x70])[0]
