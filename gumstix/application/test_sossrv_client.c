
// include files(for uart communication)
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>

// include file(for MOTE communication)

#include <sossrv_client.h>
#include <mod_pid.h>
#include "XMLFormat.h"  // XML format file for http://sensorbase.org : account : kimyh@ucla.edu


//------------------------------------------------------------------
// CONSTANTS
//------------------------------------------------------------------
#define MSG_PC_TO_MOTE  33

// Younghun //
// Message Definition

typedef struct {
  uint8_t CMD;
  uint8_t ALPHA;
  uint8_t BETA;
  uint8_t GAMMA;
  uint8_t R;
} MsgSetData;

// typedef struct{
// 	uint16_t Xi;
// 	uint16_t data;
// } MsgFromMote;


typedef struct{
	uint8_t Xi;
	uint8_t Di;
	uint8_t time;
} RawData;


//------------------------------------------------------------------
// STATIC FUNCTIONS
//------------------------------------------------------------------
static int printsosmsg(Message* psosmsg);
static int sos_msg_dispatcher();



//STATIC VARIABLES
static int no_of_receive_photo=0;  // Will receive 5 sample data from MOTE
static int no_of_receive_temp=0;  // Will receive 5 sample data from MOTE
static int no_of_receive_accx=0;
static int no_of_receive_accy=0;

static uint16_t *light;
static uint16_t *temperature;
static uint16_t *accelx;
static uint16_t *accely;
static uint16_t ID;
static char* ToDay;

static uint16_t temp_light=0;
static uint16_t temp_temperature=0;
static uint16_t temp_accelx=0;
static uint16_t temp_accely=0;
static uint16_t temp_ID=0;


//XML table function
void GPS_create(char *,uint16_t,uint16_t,uint16_t,uint16_t,uint16_t,char *);



// serial setting

  /* Baudrate setting defined at <asm/termbits.h> 
  /* <asm/termbits.h> is included at <termios.h>*/
#define BAUDRATE B4800
  /* PORT SETTING COM1="/dev/ttyS1, COM2="/dev/ttyS2 */
#define MODEMDEVICE "/dev/ttyS3"  // for gumstix
#define _POSIX_SOURCE 1 /* POSIX */

#define FALSE 0
#define TRUE 1

volatile int STOP=FALSE;

#define GPGGA "$GPGGA,"

// XML form  here will be GPS, SENSOR, plus TIME?

#define XMLF "<table><row><field name=\"field1\">"
#define XMLM "</field><field name=\"field2\">"
#define XMLL "</field></row></table>"

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




//------------------------------------------------------------------
int main(int argc, char *argv[])
{
	FILE *f;
// Zero step initialize ddd.xml file.   open table <table>
	f=fopen("./ddd.xml","wt");
	fputs(TABLE,f);
	fclose(f);	
// First PART : DATA FROM GPS
// Basically start with opening ttyS3 with baudrate 4800 and 8-N-1 without HWcontrol

    int fd,c, res;
    struct termios oldtio,newtio;
    char buf[255];
    char *gps;
    char *valid;
    int gpgga_counter=0;

    char today[10]="120706";


	printf("Enter date(mmddyy)\n");
	scanf("%s",today);



  /* 
  OPEN ttyS3 RW mode  GPS is connected to ttyS3
  */
   fd = open(MODEMDEVICE, O_RDWR | O_NOCTTY );
   if (fd <0) {perror(MODEMDEVICE); exit(-1); }

   tcgetattr(fd,&oldtio); /* save current serial port settings */
   bzero(&newtio, sizeof(newtio)); /* clear struct for new port settings */

  /*
    BAUDRATE: 4800
    CRTSCTS : NO HWctrl
    CS8     : 8N1 (8bit, no parity, 1 stopbit)
    CLOCAL  : Local connection. 
    CREAD   : enable char communication
  */
   newtio.c_cflag = BAUDRATE | CRTSCTS | CS8 | CLOCAL | CREAD;

  /*
   IGNPAR   : NO Parity 
   ICRNL    : CR->NL
    otherwise make device raw (no other input processing)
  */
   newtio.c_iflag = IGNPAR | ICRNL;

  /*
   Raw output.
  */
   newtio.c_oflag = 0;
  /*
   ICANON   : canonical IO
    disable all echo functionality, and don't send signals to calling program
  */
   newtio.c_lflag = ICANON;

  /*
  VARIABLES Initialization
  */
   newtio.c_cc[VINTR]    = 0;     /* Ctrl-c */
   newtio.c_cc[VQUIT]    = 0;     /* Ctrl-\ */
   newtio.c_cc[VERASE]   = 0;     /* del */
   newtio.c_cc[VKILL]    = 0;     /* @ */
   newtio.c_cc[VEOF]     = 4;     /* Ctrl-d */
   newtio.c_cc[VTIME]    = 0;     /* inter-character timer unused */
   newtio.c_cc[VMIN]     = 1;     /* blocking read until 1 character arrives */
   newtio.c_cc[VSWTC]    = 0;     /* '\0' */
   newtio.c_cc[VSTART]   = 0;     /* Ctrl-q */
   newtio.c_cc[VSTOP]    = 0;     /* Ctrl-s */
   newtio.c_cc[VSUSP]    = 0;     /* Ctrl-z */
   newtio.c_cc[VEOL]     = 0;     /* '\0' */
   newtio.c_cc[VREPRINT] = 0;     /* Ctrl-r */
   newtio.c_cc[VDISCARD] = 0;     /* Ctrl-u */
   newtio.c_cc[VWERASE]  = 0;     /* Ctrl-w */
   newtio.c_cc[VLNEXT]   = 0;     /* Ctrl-v */
   newtio.c_cc[VEOL2]    = 0;     /* '\0' */

  /*
    PORT INITIALIZATION and OPEN
  */
   tcflush(fd, TCIFLUSH);
   tcsetattr(fd,TCSANOW,&newtio);

  /*
  
  start to receive GPS data from GM862+GPS
  */

  // This while loop should be stoped when valid GPS data comes
  // One proposal, inserting parsing part and then if GPS is correct then
  // break also TIMEout->break(find it how to implement it.)
  printf("bbbb");
   while (STOP==FALSE) {     
	   
	   
      res = read(fd,buf,255);  // THIS is GPS data from GM862
      buf[res]=0;             /* set end of string, so we can printf */
      printf(":%s:%d\n", buf, res);
      gps=strstr(buf,GPGGA);
      if (gps!=NULL)          // GPGGA : fixed data. if this is valid -> start to parse
      {
	      gpgga_counter=gpgga_counter+1;
	      printf("GUMSTIX has %d iteration to get GPS data\n",gpgga_counter);
	      
	      valid=strstr(gps,",N,");

	      if (valid!=NULL)   // if got valid gps data then exit
	      {
			  printf("Got Valid GPS data\n Start to parse");   // this routine is only valid for north hemisphere, later on, modification needed.
		      break;
		  }
	      valid=strstr(gps,",S,");

	      if (valid!=NULL)   // if got valid gps data then exit
	      {
			  printf("Got Valid GPS data\n Start to parse");   // this routine is only valid for south hemisphere, later on, modification needed.
		      break;
		  }
	      
	      if (gpgga_counter>=10)  // if got nothing valid through 20 iteration then exit. This is similar to timeout scheme. 
	      {
		      gps="$GPGGA,000000.000,0000.0000,N,00000.0000,E,1,10,0.9,00.0,M,000.0,M,,*47";
			  printf("Cannot find 3 or more satellites\nReturns invalid data\n");   
    	      break;
		  }
	  }
	     
      if (buf[0]=='z') STOP=TRUE;
   }
   /* restore the old port settings */
    tcsetattr(fd,TCSANOW,&oldtio);
	printf("%s\n",gps);
    // we got GPGGA data now as gps pointer
    // before this let's malloc for all pointers;
    // MAYBE WE DON'T NEED MALLOC UNDER 10.
/*    
char *test;
char *test2;
char *test3;
test3=malloc(6*sizeof(char));
test=strchr(buf,',')+1;
printf("%s\n",test);
test2=strchr(test,',')+1;
printf("%s\n",test2);
strncpy(test3,test,test2-test-1); // Latitude
printf("%s\n",test3);
*/
	printf("Get Sensor and GPS Data Completed");   
/*	char *Latitude;
	char *Longitude;
	char *Altitude;
	char *Geoid;
	char *TimeStamp;
*/   
  //here after,
  //Convert parsed GPS data(Latitude and Longitude only) into XML format
  //which fits to http://sensorbase.org data base.(Predetermined format)
  	
	
	


	
	
	
// Second part sensordata parsing
	// first allocate memory for light
	light=malloc(5*sizeof(uint16_t));
	temperature=malloc(5*sizeof(uint16_t));
	accelx=malloc(5*sizeof(uint16_t));
	accely=malloc(5*sizeof(uint16_t));
/*static int no_of_receive_photo=0;  // Will receive 5 sample data from MOTE
static int no_of_receive_temp=0;  // Will receive 5 sample data from MOTE
static int no_of_receive_accx=0;
static int no_of_receive_accy=0;
*/
	if ((argc != 1) && (argc != 3)){ 
		printf("Usage Error!\n");
		printf("test_sossrv <server address> <server port>\n");
		return -1;
	}

	// Connect to the SOS server
	if (argc == 3) { 
		sossrv_connect(argv[1], argv[2]);
	} else {
		sossrv_connect(DEFAULT_IP_ADDR, DEFAULT_PORT);
	}

  // Setup the handler to receive SOS Messages
  if (sossrv_recv_msg(printsosmsg) < 0){
    printf("Setting up handler before connecting.\n");
  }
  int i=0;
  // Message Dispatcher
  //sos_msg_dispatcher();
  //for (i=0;i<10;i++)
	while(1)
	{
		if((no_of_receive_accy+no_of_receive_accx+no_of_receive_temp+no_of_receive_photo) == 24)
		{break;}	
	}
// GPS_create(gps,light,accelx,accely,ID,date) Create XML file.
	temp_light=light[0];
	temp_temperature=temperature[0];
	temp_accelx=accelx[0];
	temp_accely=accely[0];
    GPS_create(gps,temp_light,temp_accelx,temp_accely,temp_temperature,10,today); // create gps xml data.

	temp_light=light[1];
	temp_temperature=temperature[1];
	temp_accelx=accelx[1];
	temp_accely=accely[1];
    GPS_create(gps,temp_light,temp_accelx,temp_accely,temp_temperature,10,today); 

	temp_light=light[2];
	temp_temperature=temperature[2];
	temp_accelx=accelx[2];
	temp_accely=accely[2];
    GPS_create(gps,temp_light,temp_accelx,temp_accely,temp_temperature,10,today); 

	temp_light=light[3];
	temp_temperature=temperature[3];
	temp_accelx=accelx[3];
	temp_accely=accely[3];
    GPS_create(gps,temp_light,temp_accelx,temp_accely,temp_temperature,10,today); 

	temp_light=light[4];
	temp_temperature=temperature[4];
	temp_accelx=accelx[4];
	temp_accely=accely[4];
    GPS_create(gps,temp_light,temp_accelx,temp_accely,temp_temperature,10,today); 

// then disconnect sossrv.


	sossrv_disconnect();


	
	// final step close ddd.xml file with </table>.
	f=fopen("./ddd.xml","a");
	fputs("</table>",f);
	fclose(f);	

return 0;

}





//------------------------------------------------------------------
// Print SOS Message
// Note - If you want to use the message, then copy it to a local buffer
// Note - The message would be automatically freed when the handler returns
//------------------------------------------------------------------
static int printsosmsg(Message* psosmsg)
{

/*static int no_of_receive_photo=0;  // Will receive 5 sample data from MOTE
static int no_of_receive_temp=0;  // Will receive 5 sample data from MOTE
static int no_of_receive_accx=0;
static int no_of_receive_accy=0;
*/
	int i;
	uint16_t temp_value=0;
	FILE *f;
	RawData *param = (RawData*) (psosmsg->data);

	printf("Src  Mod Id: %d\n", psosmsg->sid);
	if((psosmsg->sid)==140 & ((no_of_receive_accx < 6) | (no_of_receive_accy < 6))) // From Accel sensor
	{

		if(param->Xi == 4) // accel x or y
		{
			temp_value=256*param->Di+param->time;
			no_of_receive_accx=no_of_receive_accx+1;
			accelx[no_of_receive_accx-1]=temp_value;
			printf("Accx %d \n",temp_value);

		}

		if(param->Xi == 5) // accel x or y
		{
			temp_value=256*param->Di+param->time;
			no_of_receive_accy=no_of_receive_accy+1;
			accely[no_of_receive_accy-1]=temp_value;
			printf("Accy %d \n",temp_value);

		}
	}

	if((psosmsg->sid)==128 & ((no_of_receive_photo < 6) | (no_of_receive_temp < 6))) // From Light Sensor
	{
		if(param->Xi == 1) // light
		{
			temp_value=256*param->Di+param->time;
			no_of_receive_photo=no_of_receive_photo+1;
			light[no_of_receive_photo-1]=temp_value;
			printf("Light value %d \n",temp_value);

		}

		if(param->Xi == 2) // temp
		{
			temp_value=256*param->Di+param->time;
			no_of_receive_temp=no_of_receive_temp+1;
			temperature[no_of_receive_temp-1]=temp_value;
			printf("Temp value %d \n",temp_value);

		}
	}
	if(no_of_receive_photo >=6)
	{
		no_of_receive_photo=6;
	}
	if(no_of_receive_temp >=6)
	{
		no_of_receive_temp=6;
	}

	if(no_of_receive_accx >= 6)
	{
		no_of_receive_accx=6;
	}
	if(no_of_receive_accy >= 6)
	{
		no_of_receive_accy=6;
	}
	
//  printf("------ECHO BACK FROM MOTE ------\n");
//  printf("Dest Mod Id: %d\n", psosmsg->did);
//  printf("Src  Mod Id: %d\n", psosmsg->sid);
//  printf("Dest Addr  : %X\n", psosmsg->daddr);
//  printf("Src  Addr  : %X\n", psosmsg->saddr);
//  printf("Msg Type   : %d\n", psosmsg->type);
//  printf("Msg Length : %d\n", psosmsg->len);
/*  printf("Msg Data:%d,%d,%d,%d, %d\n ",param->CMD,param->ALPHA,param->BETA,param->GAMMA,param->R);
  psosmsg->data[psosmsg->len] = '\0';
  printf("%s\n",psosmsg->data);*/
  //printf("Sensor Raw Data : %d \n",param->Xi);
  //printf("Sensor Detection Data : %d \n",param->Di);
  //printf("Time Stamp : %d \n",param->time/2);
/*  if(no_of_receive==1)
	{
		f=fopen("./ddd2.xml","a");
		if(f!=NULL)
		{
			fputs(FIELD,f);
			fputs("data1",f);
			fputs(CLOSE,f);
			fprintf(f,"%d",param->Xi);
			fputs(FIELD2,f);
		}
		fclose(f);
		light[no_of_receive-1]=param->Xi;
	}
	if(no_of_receive>1 && no_of_receive<5)
	{
		f=fopen("./ddd2.xml","a");
		if(f!=NULL)
		{
			fputs(FIELD,f);
			fputs("data",f);
			fprintf(f,"%d",no_of_receive);
			fputs(CLOSE,f);
			fprintf(f,"%d",param->Xi);
			fputs(FIELD2,f);
		}
		fclose(f);
		light[no_of_receive-1]=param->Xi;
	}
	if(no_of_receive == 5)
	{
		f=fopen("./ddd2.xml","a");
		if(f!=NULL)
		{
			fputs(FIELD,f);
			fputs("data",f);
			fputs(CLOSE,f);
			fprintf(f,"%d",param->Xi);
			fputs(FIELD2,f);
		}
		fclose(f);
		light[no_of_receive-1]=param->Xi;
	}
	
*/			
    return 0;
}


//------------------------------------------------------------------
// SOS Message Dispatcher
//------------------------------------------------------------------
static int sos_msg_dispatcher()
{
  uint8_t charbuff[127];
  uint8_t len;
  uint8_t ChangeMode; // Part 8 : 1 Set up Parameters, 2 Start Detection, 3 Stop Detection
  uint8_t ALPHA;
  uint8_t BETA;
  uint8_t GAMMA;
  uint8_t R;
  uint8_t start[127];
	uint8_t flag=0;
//  uint8_t MsgType;
  uint8_t yes[]="yes";
  MsgSetData s;
  MsgSetData *ss;  	
  
  while (1){
    printf("Command\n ");
    printf("1 : Set up parameters \n");
    printf("2 : Start Detection \n");
    printf("3 : Stop Detection \n");
    scanf("%d",&ChangeMode);

/* Message Data.(This may need a simple structure that contains commands(change variables etc. )
   data.(i.e for change variables cmd,alpha,beta,gamma,r and n)
        (or for change detection status cmd)
*/     
    switch (ChangeMode)
    {

			case 1:
	    
		    printf("1/ALPHA [1,inf)?\n");
		    scanf("%d",&s.ALPHA);
		    printf("1/BETA [1,inf) so that BETA>ALPHA?\n");
		    scanf("%d",&s.BETA);
		    printf("GAMMA (0,inf.)?\n");
		    scanf("%d",&s.GAMMA);
		    printf("R(Hz) [1,20]?\n");
		    scanf("%d",&s.R);
				s.CMD =(uint8_t) 1;
				flag=1;
				break;
	    

			case 2:
	    
		    printf("Start Detection?(yes/no)\n");
		    scanf("%s",start);
//		    if(strcmp(start,yes)==0)
//		    {
		    s.CMD = 2;
		    s.ALPHA = 0;
		    s.BETA = 0;
		    s.GAMMA = 0;
		    s.R = 0;
				flag=1;
//		    }
		    
				break;
	    
	    
	    case 3:
	    
		    printf("Stop Detection?(yes/no)");
		    scanf("%s",start);
//		    if(strcmp(start,yes)==0)
//		    {
		    s.CMD = 3;
		    s.ALPHA = 0;
		    s.BETA = 0;
		    s.GAMMA = 0;
		    s.R = 0;
				flag=1;
//		    }
				break;
	    

			default:
			break;
    }
    
		    

    //len = sizeof(s);
    printf("Sending %d bytes to the sensor network ...\n", len);
	  printf("CMD=%d\n",s.CMD);
	  printf("ALPHA=1/%d\n",s.ALPHA);
	  printf("BETA=1/%d\n",s.BETA);
	  printf("GAMMA=%d\n",s.GAMMA);
	  printf("R=%dHz\n",s.R);
    ss=&s;
		if(flag==1){
    sossrv_post_msg(
			DFLT_APP_ID1, 
			DFLT_APP_ID1, 
			MSG_PC_TO_MOTE, 
			5, 
			(void *)ss, 
			65534, 
			65535);}
		flag=0;
			}
  return 0;
}
// GPS table creation function
void GPS_create(char *gps,uint16_t light,uint16_t accelx, uint16_t accely,uint16_t temperature, uint16_t ID,char *date)
{
    char *finding;
    char *finding2;
	char *Latitude;
	char *Longitude;
	char *Altitude;
	char *Geoid;
	char *TimeStamp;
    

	finding=strchr(gps,',')+1;
	finding2=strchr(finding,',')-1;
    TimeStamp=malloc((finding2-finding+1+1)*sizeof(char));
    strncpy(TimeStamp,finding,finding2-finding+1);  // TimeStamp hhmmss
    TimeStamp[(finding2-finding+1)]='\0';

    finding=strchr(gps,',')+1;
    finding=strchr(finding,',')+1;
    finding2=strchr(finding,',')+1;
    Latitude=malloc((finding2-finding+1+1)*sizeof(char));
    strncpy(Latitude,finding,finding2-finding+1); // Latitude
    Latitude[(finding2-finding+1)]='\0';

    finding=strchr(finding,',')+1;
    finding=strchr(finding,',')+1;
    finding2=strchr(finding,',')+1;
    Longitude=malloc((finding2-finding+1+1)*sizeof(char));
    strncpy(Longitude,finding,finding2-finding+1); // Longitude
    Longitude[(finding2-finding+1)]='\0';

    finding=strchr(finding,',')+1;
    finding=strchr(finding,',')+1;
    finding=strchr(finding,',')+1;
    finding=strchr(finding,',')+1;

    finding=strchr(finding,',')+1;
    finding2=strchr(finding,',')+1;
    Altitude=malloc((finding2-finding+1+1)*sizeof(char));
    strncpy(Altitude,finding,finding2-finding+1); // Altitude
    Altitude[(finding2-finding+1)]='\0';

    finding=strchr(finding,',')+1;
    finding=strchr(finding,',')+1;
    finding2=strchr(finding,',')+1;
    Geoid=malloc((finding2-finding+1+1)*sizeof(char));
    strncpy(Geoid,finding,finding2-finding+1); // Geoid
    Geoid[(finding2-finding+1)]='\0';


	FILE *f;
	f=fopen("./ddd.xml","a"); // this should be replaced by something "wt"
	fputs(ROW,f); // start row here ( <row> ) xml
	
	// TimeStamp

	fputs(FIELD,f);
	fputs("TimeStamp",f);
	fputs(CLOSE,f);
	fputs(TimeStamp,f);
	fputs(FIELD2,f);

	// Latitude
	fputs(FIELD,f);
	fputs("Latitude",f);
	fputs(CLOSE,f);
	fputs(Latitude,f);
	fputs(FIELD2,f);

	// Longitude
	fputs(FIELD,f);
	fputs("Longitude",f);
	fputs(CLOSE,f);
	fputs(Longitude,f);
	fputs(FIELD2,f);

	// Altitude
	fputs(FIELD,f);
	fputs("Altitude",f);
	fputs(CLOSE,f);
	fputs(Altitude,f);
	fputs(FIELD2,f);

	// Geoid
	fputs(FIELD,f);
	fputs("Geoid",f);
	fputs(CLOSE,f);
	fputs(Geoid,f);
	fputs(FIELD2,f);

	// Light
	fputs(FIELD,f);
	fputs("LightLevel",f);
	fputs(CLOSE,f);
	fprintf(f,"%d",light);
	fputs(FIELD2,f);

	// Accelx
	fputs(FIELD,f);
	fputs("Accelx",f);
	fputs(CLOSE,f);
	fprintf(f,"%d",accelx);
	fputs(FIELD2,f);

	// Accely
	fputs(FIELD,f);
	fputs("Accely",f);
	fputs(CLOSE,f);
	fprintf(f,"%d",accely);
	fputs(FIELD2,f);

	// Temperature
	fputs(FIELD,f);
	fputs("Temperature",f);
	fputs(CLOSE,f);
	fprintf(f,"%d",temperature);
	fputs(FIELD2,f);


	// MoteID
	fputs(FIELD,f);
	fputs("MoteID",f);
	fputs(CLOSE,f);
	fprintf(f,"%d",ID);
	fputs(FIELD2,f);

	// Date
	fputs(FIELD,f);
	fputs("Date",f);
	fputs(CLOSE,f);
	fprintf(f,"%s",date);
	fputs(FIELD2,f);
	fputs(ROWn,f);
	
	fclose(f);
//free all the pointers

   	free(Latitude); // Latitude
	free(Longitude);  // Longitude
	free(Altitude);  // Altitude
	free(Geoid);  // Geoid
	free(TimeStamp);  // TimeStamp hhmmss

	return;
}

