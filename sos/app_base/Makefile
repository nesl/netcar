PROJ = main_app
ROOTDIR = $(SOSROOT)

SRCS += accel_sampler.c loader.c nic.c rats.c linear.c

ifneq ($(SKIP_ACCEL), 1)
SRCS += accel_sensor.c
endif

INCDIR += -I$(ROOTDIR)/modules/sensordrivers/h34c/include/ -I../modules
SB = h34c

include $(ROOTDIR)/config/Makerules

vpath loader.c $(ROOTDIR)/extensions/loader/
vpath nic.c $(ROOTDIR)/modules/management/nic/
vpath rats.c $(ROOTDIR)/extensions/rats
vpath linear.c $(ROOTDIR)/extensions/rats
vpath accel_sampler.c ../modules/
vpath accel_sensor.c $(ROOTDIR)/modules/sensordrivers/h34c/accel/
