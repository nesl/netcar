PROJ = main_app
ROOTDIR = $(SOS_DIR)

DEFS += -DMTS310SB
SRCS += accel_sampler.c accel_sensor.c loader.c nic.c
INCDIR += -I$(ROOTDIR)/modules/sensordrivers/mts310/include/ -I../modules
SB = mts310

include $(ROOTDIR)/config/Makerules

vpath loader.c $(ROOTDIR)/modules/management/loader/
vpath nic.c $(ROOTDIR)/modules/management/nic/
vpath accel_sampler.c ../modules/
vpath accel_sensor.c $(ROOTDIR)modules/sensordrivers/mts310/accel/