# Database layouts

## MongoDB
All the data for the application uses the `iotwarden` database.

It has the collections:
- White/Black List (whiteblacklist)
- Packets (packets)

### Collection Schemes
#### White Black List
```json
{
    "_id": ObjectId(...),
    "ip": <ip>,
    "allowed": <true|false>
}
```

#### Packets
```json
{
    "_id": ObjectId(...),
    "protocols": <dict from framedissect>,
    "total_header_len": <header len in bytes>
    "raw_contents": <raw bytes without headers>
}
```

## Redis
Cache data for the application

It contains the following types of key-value pairs:
- White/Black List (list)
- Packets (packet)

### White/Black List
```text
list_<ip-address>: <true|false>
```

### Packet
```text
packet_<uuid>: <Packet document as seen above in MongoDB, just with no '_id'>
```
