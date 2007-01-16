/* -*- Mode: C; tab-width:2 -*- */
/* ex: set ts=2 shiftwidth=2 softtabstop=2 cindent: */

#include <module.h>
#include <sys_module.h>
#include <string.h>

#define LED_DEBUG
#include <led_dbg.h>

#include <mts310sb.h>

#define ACCEL_TEST_APP_TID 0
#define ACCEL_TEST_APP_INTERVAL 40

#define ACCEL_TEST_PID DFLT_APP_ID0

#define UART_MSG_LEN 3

#define SAMPLES_PER_MSG 5
#define MSG_LENGTH (SAMPLES_PER_MSG * 2)
#define MSG_ACCEL_DATA 41

enum {
	ACCEL_TEST_APP_INIT=0,
	ACCEL_TEST_APP_IDLE,
	ACCEL_TEST_APP_ACCEL_0,
	ACCEL_TEST_APP_ACCEL_0_BUSY,
	ACCEL_TEST_APP_ACCEL_1,
	ACCEL_TEST_APP_ACCEL_1_BUSY,
};

typedef struct {
	uint8_t pid;
	uint8_t state;
	uint8_t sample_nr;
	uint16_t accel0[SAMPLES_PER_MSG];
	uint16_t accel1[SAMPLES_PER_MSG];
} app_state_t;


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
			//allocate the space for the accelerometers
			ker_timer_init(s->pid, ACCEL_TEST_APP_TID, TIMER_REPEAT);
			if(ker_id() != 0){
				ker_timer_start(s->pid, ACCEL_TEST_APP_TID, ACCEL_TEST_APP_INTERVAL);
			}
			ker_sensor_enable(s->pid, MTS310_ACCEL_0_SID);
			break;

		case MSG_FINAL:
			ker_sensor_disable(s->pid, MTS310_ACCEL_0_SID);
			break;

		case MSG_TIMER_TIMEOUT:
			{
				LED_DBG(LED_YELLOW_TOGGLE);
				switch (s->state) {
				case ACCEL_TEST_APP_INIT:
					// do any necessary init here
					s->state = ACCEL_TEST_APP_IDLE;
					break;
					
				case ACCEL_TEST_APP_IDLE:
					s->state = ACCEL_TEST_APP_ACCEL_0;
					break;
					
				case ACCEL_TEST_APP_ACCEL_0:
					s->state = ACCEL_TEST_APP_ACCEL_0_BUSY;
					ker_sensor_get_data(s->pid, MTS310_ACCEL_0_SID);
					break;
					
				case ACCEL_TEST_APP_ACCEL_1:
					break;
					
					//ignore the sampling if we are still busy
				case ACCEL_TEST_APP_ACCEL_0_BUSY:
					break;
				case ACCEL_TEST_APP_ACCEL_1_BUSY:
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
					ker_sensor_get_data(s->pid, MTS310_ACCEL_1_SID);		
					s->state = ACCEL_TEST_APP_ACCEL_1_BUSY;
					break;

				case ACCEL_TEST_APP_ACCEL_1_BUSY:
					// second accel sampled, wait for timeout and go back to accel 0
					if(s->sample_nr < SAMPLES_PER_MSG) {
						s->accel1[s->sample_nr] = m->byte;
					} else {
						LED_DBG(LED_RED_TOGGLE);
					}
					s->sample_nr++;
					if(s->sample_nr >= SAMPLES_PER_MSG){
						//we collected enough samples, send out a message
						uint8_t *data_msg;
					
						s->sample_nr = 0;
						
						data_msg = sys_malloc (2 * MSG_LENGTH);
						
						if ( data_msg ) {
							memcpy((void*)&(data_msg[0]), (void*)s->accel0, MSG_LENGTH);
							memcpy((void*)&(data_msg[MSG_LENGTH]), (void*)s->accel1, MSG_LENGTH);

							sys_post_net ( s->pid,
														 MSG_ACCEL_DATA,
														 2*MSG_LENGTH,
														 data_msg,
														 SOS_MSG_RELEASE,
														 BCAST_ADDRESS);
						} else {
							LED_DBG(LED_RED_TOGGLE);
						}
					}

					s->state = ACCEL_TEST_APP_ACCEL_0;
					break;

				default:
					LED_DBG(LED_RED_TOGGLE);
					s->state = ACCEL_TEST_APP_INIT;
					break;
				}

			}
			break;

	case MSG_ACCEL_DATA:
		if(ker_id() == 0) {
			LED_DBG(LED_GREEN_TOGGLE);
						
			sys_post_uart ( s->pid,
										 MSG_ACCEL_DATA,
										 2*MSG_LENGTH,
										 msg->data,
										 SOS_MSG_RELEASE,
										 UART_ADDRESS);
			
		}
	default:
		return -EINVAL;
		break;
	}
	return SOS_OK;
}

mod_header_ptr accel_test_app_get_header() {
	return sos_get_header_address(mod_header);
}


