# Game Data Serialization Formats

## Format Comparison

| Format | Speed | Size | Schema | Language Support |
|--------|-------|------|--------|------------------|
| JSON | Slow | Large | No | Universal |
| MessagePack | Fast | Small | No | Wide |
| Protocol Buffers | Fast | Tiny | Yes | Wide |
| FlatBuffers | Fastest | Tiny | Yes | Moderate |

## Recommendations

### For Player State Updates (60 Hz)
- **Use FlatBuffers or Protocol Buffers**
- Pre-allocate buffers
- Zero-copy deserialization

### For Chat/Lobby Data
- **Use JSON** for debugging ease
- MessagePack for production

### For Save Games
- **Use Protocol Buffers**
- Schema evolution support
- Backwards compatibility

## Sample Protobuf Schema
```protobuf
message PlayerState {
  int32 id = 1;
  float x = 2;
  float y = 3;
  int32 health = 4;
}
```
