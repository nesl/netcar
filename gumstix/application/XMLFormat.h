

// XML form  here will be GPS, SENSOR, plus TIME?

#define XMLF "<table><row><field name=\"field1\">"
#define XMLM "</field><field name=\"field2\">"
#define XMLL "</field></row></table>"
#define TABLE "<table>"
#define TABLEn "</table>"
#define ROW "<row>"
#define ROWn "</row>"
#define FIELD "<field name=\""
#define CLOSE "\">"
#define FIELD2 "</field>"
#define XMLEND "</row></table>"
#define TIME "Time"

// GPS FIXED DATA

#define GPGGA "$GPGGA,"



//<table><row><field name="field1">10000</field><field name="field2">10000</field></row></table>
// I'll cut 4807.038N, 01131.000,E
// REMEMBER itoa()

/*
$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47

Where:
     GGA          Global Positioning System Fix Data
     123519       Fix taken at 12:35:19 UTC
     4807.038,N   Latitude 48 deg 07.038' N
     01131.000,E  Longitude 11 deg 31.000' E
     1            Fix quality: 0 = invalid
                               1 = GPS fix (SPS)
                               2 = DGPS fix
                               3 = PPS fix
			       4 = Real Time Kinematic
			       5 = Float RTK
                               6 = estimated (dead reckoning) (2.3 feature)
			       7 = Manual input mode
			       8 = Simulation mode
     08           Number of satellites being tracked
     0.9          Horizontal dilution of position
     545.4,M      Altitude, Meters, above mean sea level
     46.9,M       Height of geoid (mean sea level) above WGS84
                      ellipsoid
     (empty field) time in seconds since last DGPS update
     (empty field) DGPS station ID number
     *47          the checksum data, always begins with *
*/
