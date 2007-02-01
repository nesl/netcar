#include <sos.h>

mod_header_ptr rats_get_header();
mod_header_ptr loader_get_header();
mod_header_ptr accel_sampler_get_header();

#ifndef SOS_SIM
mod_header_ptr accel_sensor_get_header();
#endif

void sos_start(void) {
  ker_register_module(loader_get_header());
  ker_register_module(rats_get_header());
#ifndef SOS_SIM
  ker_register_module(accel_sensor_get_header());
#endif
  ker_register_module(accel_sampler_get_header());
}
