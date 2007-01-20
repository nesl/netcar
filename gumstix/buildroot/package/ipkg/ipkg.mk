#############################################################
#
# ipkgf
#
#############################################################
IPKG_NAME:=ipkg-utils
IPKG_VERSION:=1.7
IPKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
IPKG_SITE:=http://handhelds.org/packages/ipkg-utils/
IPKG_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
IPKG_CAT:=zcat
IPKG_BINARY:=ipkg/ipkg
IPKG_TARGET_BINARY:=usr/sbin/ipkg


$(DL_DIR)/$(IPKG_SOURCE):
	 $(WGET) -P $(DL_DIR) $(IPKG_SITE)/$(IPKG_SOURCE)

ipkg-source: $(DL_DIR)/$(IPKG_SOURCE)

$(IPKG_DIR)/.unpacked: $(DL_DIR)/$(IPKG_SOURCE)
	$(IPKG_CAT) $(DL_DIR)/$(IPKG_SOURCE) | tar -C $(BUILD_DIR) $(TAR_OPTIONS) -
	$(SED) 's/ -DIPX_CHANGE -DHAVE_MMAP//' $(IPKG_DIR)/ipkg/Makefile.linux
	$(SED) 's/HAVE_MULTILINK=y/#HAVE_MULTILINK=y/' $(IPKG_DIR)/ipkg/Makefile.linux
	$(SED) 's/FILTER=y/#FILTER=y/' $(IPKG_DIR)/ipkg/Makefile.linux
	$(SED) 's,(INSTALL) -s,(INSTALL),' $(IPKG_DIR)/*/Makefile.linux
	$(SED) 's,(INSTALL) -s,(INSTALL),' $(IPKG_DIR)/ipkg/plugins/*/Makefile.linux
	$(SED) 's/ -o root//' $(IPKG_DIR)/*/Makefile.linux
	$(SED) 's/ -g daemon//' $(IPKG_DIR)/*/Makefile.linux
	touch $(IPKG_DIR)/.unpacked

$(IPKG_DIR)/.configured: $(IPKG_DIR)/.unpacked
	(cd $(IPKG_DIR); rm -rf config.cache; \
		$(TARGET_CONFIGURE_OPTS) \
		./configure \
		--target=$(GNU_TARGET_NAME) \
		--host=$(GNU_TARGET_NAME) \
		--build=$(GNU_HOST_NAME) \
		--prefix=/usr \
		--exec-prefix=/usr \
		--bindir=/usr/bin \
		--sbindir=/usr/sbin \
		--libexecdir=/usr/lib \
		--sysconfdir=/etc \
		--datadir=/usr/share \
		--localstatedir=/var \
		--mandir=/usr/man \
		--infodir=/usr/info \
		$(DISABLE_NLS) \
	);
	touch $(IPKG_DIR)/.configured

$(IPKG_DIR)/$(IPKG_BINARY): $(IPKG_DIR)/.configured
	$(MAKE) CC=$(TARGET_CC) -C $(IPKG_DIR)

$(TARGET_DIR)/$(IPKG_TARGET_BINARY): $(IPKG_DIR)/$(IPKG_BINARY)
	$(MAKE1) DESTDIR=$(TARGET_DIR)/usr CC=$(TARGET_CC) -C $(IPKG_DIR) install
	rm -rf $(TARGET_DIR)/usr/share/locale $(TARGET_DIR)/usr/info \
		$(TARGET_DIR)/usr/man $(TARGET_DIR)/usr/share/doc

ipkg: uclibc $(TARGET_DIR)/$(IPKG_TARGET_BINARY)

ipkg-clean:
	rm -f  $(TARGET_DIR)/usr/sbin/ipkg
	rm -f  $(TARGET_DIR)/usr/sbin/chat
	rm -rf $(TARGET_DIR)/etc/ppp
	$(MAKE) DESTDIR=$(TARGET_DIR)/usr CC=$(TARGET_CC) -C $(IPKG_DIR) uninstall
	-$(MAKE) -C $(IPKG_DIR) clean

ipkg-dirclean:
	rm -rf $(IPKG_DIR)


#############################################################
#
# Toplevel Makefile options
#
#############################################################
ifeq ($(strip $(BR2_PACKAGE_IPKG)),y)
TARGETS+=ipkg
endif



