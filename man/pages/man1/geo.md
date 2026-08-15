# geo - Geolocation Engine [GODMODE]

## NAME

geo - Geolocation Engine [GODMODE] - IP geolocation, reverse geocoding, batch queries

## DESCRIPTION

The geo command provides access to TerminalX's advanced geolocation engine. This GODMODE system supports IP geolocation, reverse geocoding, batch queries, GPS daemon, map engine, and fusion engine with multiple providers and caching.

## SYNOPSIS

```
geo locate <query> [provider]
geo ip <query> [provider]
geo reverse <lat> <lon>
geo batch <query1> <query2> ...
geo providers
geo stats
geo cache <clear|size|info>
geo plugins
geo config [key=value]
geo gps <status|start|stop|enable|disable>
geo map <status|enable|disable|render> [lat] [lon] [zoom] [size]
geo fusion <status|enable|disable>
```

## OPTIONS

- `locate <query> [provider]` - Locate an IP address or location
- `ip <query> [provider]` - Alias for locate
- `reverse <lat> <lon>` - Reverse geocode coordinates
- `batch <query1> <query2> ...` - Locate multiple queries in parallel
- `providers` - List available providers
- `stats` - Show geo engine statistics
- `cache <clear|size|info>` - Cache management commands
- `plugins` - List active plugins
- `config [key=value]` - Show or update configuration
- `gps <status|start|stop|enable|disable>` - GPS daemon commands
- `map <status|enable|disable|render>` - Map engine commands
- `fusion <status|enable|disable>` - Fusion engine commands

## EXAMPLES

### Geolocation
```
geo locate 8.8.8.8
geo ip 1.1.1.1
geo reverse 40.7128 -74.0060
geo batch 8.8.8.8 1.1.1.1 8.8.4.4
```

### Management
```
geo providers
geo stats
geo plugins
geo config timeout=15
```

### Cache
```
geo cache clear
geo cache size
geo cache info
```

### GPS Daemon (v5)
```
geo gps enable
geo gps start
geo gps status
geo gps stop
geo gps disable
```

### Map Engine (v6)
```
geo map enable osm
geo map status
geo map render 52.0 21.0 15 512
geo map disable
```

### Fusion Engine (v6)
```
geo fusion enable
geo fusion status
geo fusion disable
```

## GPS DAEMON (v5)

The GPS daemon provides real-time location tracking with the following features:

- **Async GPS Loop**: Continuous location updates
- **Mock or Real GPS Provider**: Configurable GPS data source
- **EventBus**: Streaming location updates to subscribers
- **Plugin System**: Extensible GPS plugins (logger, recorder, etc.)
- **Thread-safe Cache**: Last position cache
- **Command Interface**: In-process GPS commands

### GPS Plugins
- **logger**: Logs GPS fixes to console
- **record**: Records GPS fixes in history
- **Custom**: Create custom plugins by extending GPSPlugin class

## MAP ENGINE (v5)

The map engine provides interactive map rendering with the following features:

- **OSM Renderer**: OpenStreetMap tile rendering (no API key required)
- **Google Renderer**: Google Static Maps rendering (API key required)
- **Map Layers**: Points, paths, and heatmaps
- **EventBus**: Streaming map updates to subscribers
- **Plugin System**: Extensible map plugins (logger, custom renderers)
- **Integration**: Seamless integration with GeoEngine and GPS daemon

### Map Features
- **Markers**: Add custom colored points on the map
- **Paths**: Draw paths between multiple coordinates
- **Heatmaps**: Display intensity-based heat maps
- **Custom Renderers**: Create custom map renderers by extending MapPlugin class

### Map Plugins
- **logger**: Logs render events to console
- **Custom**: Create custom plugins by extending MapPlugin class

## FUSION ENGINE (v6)

The fusion engine provides unified location tracking combining multiple sources:

- **Weighted Fusion**: Combines GPS, BTS, and WiFi positioning
- **Confidence Scoring**: Calculates confidence based on source count and accuracy
- **EventBus**: Streaming fusion updates to subscribers
- **Plugin System**: Extensible fusion plugins (logger, recorder, bridges)
- **Integration**: Seamless integration with GeoEngine and MapEngine

### Fusion Features
- **GPS Integration**: Real-time GPS data input
- **BTS Triangulation**: Cell tower location input
- **WiFi Positioning**: WiFi-based location input
- **Weighted Averaging**: Configurable weights for each source
- **Confidence Calculation**: Multi-source confidence scoring

### Fusion Plugins
- **logger**: Logs fusion results to console
- **record**: Records fusion history
- **Custom**: Create custom plugins by extending FusionPlugin class

## SEE ALSO

man(1), net(1), network(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
