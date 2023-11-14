# Database layouts

## MongoDB
All the data for the application uses the `iotwarden` database.

It has the collections:
- White/Black List (whiteblacklist)
- Commands (commands)
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
