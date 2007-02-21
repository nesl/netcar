/* -*- Mode: C; tab-width:2 -*- */
/* ex: set ts=2 shiftwidth=2 softtabstop=2 cindent: */

#include <module.h>
#include <sys_module.h>
#include <string.h>
#include <rats/rats.h>

#define LED_DEBUG
#include <led_dbg.h>

#include <h34c.h>

#define ACCEL_TEST_APP_TID 0
#ifdef SOS_SIM
#define ACCEL_TEST_APP_INTERVAL 50
#else
#define ACCEL_TEST_APP_INTERVAL 10
#endif

#define ACCEL_TEST_PID DFLT_APP_ID0

#define SAMPLES_PER_MSG 10

#define MSG_ACCEL_DATA (MOD_MSG_START + 1)
#define ROOT_ID 0
//the following message is used for the RATS reply
#define MSG_REPLY (MOD_MSG_START + 0)


enum {
	ACCEL_TEST_APP_INIT=0,
	ACCEL_TEST_APP_IDLE,
	ACCEL_TEST_APP_ACCEL_0,
	ACCEL_TEST_APP_ACCEL_0_BUSY,
	ACCEL_TEST_APP_ACCEL_1,
	ACCEL_TEST_APP_ACCEL_1_BUSY,
	ACCEL_TEST_APP_ACCEL_2,
	ACCEL_TEST_APP_ACCEL_2_BUSY,
};

typedef struct {
	uint8_t pid;
	uint8_t state;
	uint8_t sample_nr;
	uint32_t seq_nr;
	uint16_t accel0[SAMPLES_PER_MSG];
	uint16_t accel1[SAMPLES_PER_MSG];
	uint16_t accel2[SAMPLES_PER_MSG];
} app_state_t;

typedef struct {
	uint32_t seq_nr;
	uint16_t accel0[SAMPLES_PER_MSG];
	uint16_t accel1[SAMPLES_PER_MSG];
	uint16_t accel2[SAMPLES_PER_MSG];
} accel_msg_t;

static int8_t accel_test_msg_handler(void *state, Message *msg);

static mod_header_t mod_header SOS_MODULE_HEADER = {
	.mod_id         = ACCEL_TEST_PID,
	.state_size     = sizeof(app_state_t),
	.num_timers     = 1,
	.num_sub_func   = 0,
	.num_prov_func  = 0,
	.platform_type = HW_TYPE,
	.processor_type = MCU_TYPE,
	.code_id = ehtons(ACCEL_TEST_PID),
	.module_handler = accel_test_msg_handler,
};


static int8_t accel_test_msg_handler(void *state, Message *msg)
{
	app_state_t *s = (app_state_t *) state;

	switch ( msg->type ) {

		case MSG_INIT:
			s->state = ACCEL_TEST_APP_INIT;
			s->pid = msg->did;
			s->sample_nr = 0;
			s->seq_nr = 0;
			//allocate the space for the accelerometers
			ker_timer_init(s->pid, ACCEL_TEST_APP_TID, TIMER_REPEAT);
			ker_timer_start(s->pid, ACCEL_TEST_APP_TID, ACCEL_TEST_APP_INTERVAL);
			ker_sensor_enable(s->pid, H34C_ACCEL_0_SID);
			//we need to start the time synchronisation process with the root id node
			if(ker_id() != ROOT_ID){
				post_short(RATS_TIMESYNC_PID, s->pid, MSG_RATS_CLIENT_START, 1, ROOT_ID, 0);
			}
			break;

		case MSG_FINAL:
			ker_sensor_disable(s->pid, H34C_ACCEL_0_SID);
			ker_timer_stop(s->pid, ACCEL_TEST_APP_TID);
			post_short(RATS_TIMESYNC_PID, s->pid, MSG_RATS_CLIENT_STOP, 0, ROOT_ID, 0);
			break;

		case MSG_TIMER_TIMEOUT:
			{
				switch (s->state) {
				case ACCEL_TEST_APP_INIT:
					// do any necessary init here
					s->state = ACCEL_TEST_APP_IDLE;
					break;
					
				case ACCEL_TEST_APP_IDLE:
					s->state = ACCEL_TEST_APP_ACCEL_0;
					break;
					
				case ACCEL_TEST_APP_ACCEL_0:
					//LED_DBG(LED_YELLOW_TOGGLE);
					s->state = ACCEL_TEST_APP_ACCEL_0_BUSY;
					ker_sensor_get_data(s->pid, H34C_ACCEL_0_SID);
#ifdef SOS_SIM
					post_short(s->pid, s->pid, MSG_DATA_READY, 0, 0xaaaa, 0);
#endif
					break;
					
				case ACCEL_TEST_APP_ACCEL_1:
					break;
					
					//ignore the sampling if we are still busy
				case ACCEL_TEST_APP_ACCEL_0_BUSY:
				case ACCEL_TEST_APP_ACCEL_1_BUSY:
				case ACCEL_TEST_APP_ACCEL_2_BUSY:
					LED_DBG(LED_GREEN_TOGGLE);
					break;

				default:
					LED_DBG(LED_RED_TOGGLE);
					s->state = ACCEL_TEST_APP_INIT;
					break;
				}
			}
			break;

		case MSG_DATA_READY:
			{
				MsgParam* m;
				m = (MsgParam*)msg->data;

				switch(s->state) {
					case ACCEL_TEST_APP_ACCEL_0_BUSY:
						// first accel sampled, sample next one
						if(s->sample_nr < SAMPLES_PER_MSG) {
							s->accel0[s->sample_nr] = m->word;
						} else {
							LED_DBG(LED_RED_TOGGLE);
						}
						s->state = ACCEL_TEST_APP_ACCEL_1_BUSY;
						ker_sensor_get_data(s->pid, H34C_ACCEL_1_SID);		
#ifdef SOS_SIM
						post_short(s->pid, s->pid, MSG_DATA_READY, 0, 0xaaaa, 0);
#endif
						break;

					case ACCEL_TEST_APP_ACCEL_1_BUSY:
						// first accel sampled, sample next one
						if(s->sample_nr < SAMPLES_PER_MSG) {
							s->accel1[s->sample_nr] = m->word;
						} else {
							LED_DBG(LED_RED_TOGGLE);
						}
						s->state = ACCEL_TEST_APP_ACCEL_2_BUSY;
						ker_sensor_get_data(s->pid, H34C_ACCEL_2_SID);		
#ifdef SOS_SIM
						post_short(s->pid, s->pid, MSG_DATA_READY, 0, 0xaaaa, 0);
#endif
						break;

				case ACCEL_TEST_APP_ACCEL_2_BUSY:
					// second accel sampled, wait for timeout and go back to accel 0
					if(s->sample_nr < SAMPLES_PER_MSG) {
						s->accel2[s->sample_nr] = m->word;
					} else {
						LED_DBG(LED_RED_TOGGLE);
					}
					s->sample_nr++;
					if(s->sample_nr >= SAMPLES_PER_MSG){
						//we collected enough samples, get the current time
						rats_t *rats_ptr = (rats_t *)sys_malloc(sizeof(rats_t));
						rats_ptr->mod_id = s->pid;
						rats_ptr->source_node_id = ker_id();
						rats_ptr->target_node_id = ROOT_ID;
						rats_ptr->time_at_source_node = ker_systime32();
						rats_ptr->msg_type = MSG_REPLY;
						if(ker_id() == ROOT_ID){
							// don't use rats for the sync. Generate the message ourself	
							rats_ptr->time_at_target_node = rats_ptr->time_at_source_node;
							post_long(s->pid, s->pid, MSG_REPLY, sizeof(rats_t), rats_ptr, SOS_MSG_RELEASE);
						} else {
							post_long(RATS_TIMESYNC_PID, s->pid, MSG_RATS_GET_TIME, sizeof(rats_t), rats_ptr, SOS_MSG_RELEASE);
						}
					} else {
						// We are not done yet. Sample the next sensor.
						s->state = ACCEL_TEST_APP_ACCEL_0;
					}
					break;
				
				default:
					LED_DBG(LED_RED_TOGGLE);
					s->state = ACCEL_TEST_APP_INIT;
					break;
				}

			}
			break;

	case MSG_REPLY:
		{
			// we received the current time from RATS. Now we can send out the message.
			accel_msg_t *data_msg;
			rats_t *rats_ptr = (rats_t *)msg->data;

			s->sample_nr = 0;
			
			data_msg = (accel_msg_t*)sys_malloc (sizeof(accel_msg_t));
			
			//we specifically don't check for an overflow since we want to start at 0 again.
			data_msg->seq_nr = rats_ptr->time_at_target_node;
			DEBUG("Sending packet with time %d\n", rats_ptr->time_at_target_node);			
			
			if ( data_msg ) {
				memcpy((void*)data_msg->accel0, (void*)s->accel0, SAMPLES_PER_MSG*sizeof(uint16_t));
				memcpy((void*)data_msg->accel1, (void*)s->accel1, SAMPLES_PER_MSG*sizeof(uint16_t));
				memcpy((void*)data_msg->accel2, (void*)s->accel2, SAMPLES_PER_MSG*sizeof(uint16_t));
				LED_DBG(LED_YELLOW_TOGGLE);
				if(ker_id() == 0){
					sys_post_uart ( s->pid,
													MSG_ACCEL_DATA,
													sizeof(accel_msg_t),
													data_msg,
													SOS_MSG_RELEASE,
													BCAST_ADDRESS);
				} else {
					sys_post_net ( s->pid,
												 MSG_ACCEL_DATA,
												 sizeof(accel_msg_t),
												 data_msg,
												 SOS_MSG_RELEASE,
												 BCAST_ADDRESS);
				}
			} else {
				LED_DBG(LED_RED_TOGGLE);
			}
			rats_ptr = NULL; //otherwise it won't compile for mica2 (rats_ptr would be unused) FIXME: why is that so?
		
		
			s->state = ACCEL_TEST_APP_ACCEL_0;
			break;
		}
			/*	
  case MSG_ACCEL_DATA:
		if(ker_id() == 0) {
			LED_DBG(LED_GREEN_TOGGLE);
						
			sys_post_uart ( s->pid,
										 MSG_ACCEL_DATA,
										 sizeof(accel_msg_t),
										 msg->data,
										 SOS_MSG_RELEASE,
										 UART_ADDRESS);
			
	 }
			*/
	default:
		return -EINVAL;
		break;
	}
	return SOS_OK;
}

mod_header_ptr accel_sampler_get_header() {
	return sos_get_header_address(mod_header);
}


