PROJ = main_app
ROOTDIR = $(SOS_DIR)

DEFS += -DMTS310SB
SRCS += accel_sampler.c loader.c rats.c linear.c

ifneq ($(SKIP_ACCEL),1)
SRCS += accel_sensor.c
endif

INCDIR += -I$(ROOTDIR)/modules/sensordrivers/mts310/include/ -I../modules
SB = mts310

include $(ROOTDIR)/config/Makerules

vpath loader.c $(ROOTDIR)/modules/management/loader/
vpath rats.c $(ROOTDIR)/extensions/rats
vpath linear.c $(ROOTDIR)/extensions/rats
vpath accel_sampler.c ../modules/
vpath accel_sensor.c $(ROOTDIR)/modules/sensordrivers/mts310/accel/
