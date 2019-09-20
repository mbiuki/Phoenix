* Real-world data set by running a PixHawk DIY drone.
* We only can show real world data set for the location where we are. We cannot show dataset for other geographical locations since demonstrting real data required us to travel to other corners of the world to collect time-series and we could not afford it.

# TLogDataExtractor
## Use TlogDataExtractor to convert tlog collected from drone at field into csv formatted files ready to be processed by Phoenix authentication service.
### For more about the TLogDataExtractor and how to use it please read here:

https://diydrones.com/profiles/blogs/extracting-data-from-tlog-files-for-plotting-in-excel

### Run the application located in: \TLogDataExtractor\TLogDataExtractor\bin\Release

### I have put some of the raw data for 10 missions that collected at field (UBC soccer field).

## Pick the following parameters:
### Altitude: mavlink_terrain_report_t.current_height
### Latitude:  mavlink_gps_raw_int_t.lat
### Longitude:  mavlink_gps_raw_int_t.lon
### Yaw:  mavlink_attitude_t.yaw
### Roll:  mavlink_attitude_t.roll
### Pitch:  mavlink_attitude_t.pitch



