# $Id: Makefile 2663 2005-12-13 19:25:22Z nbd $

include $(TOPDIR)/rules.mk

PKG_NAME:=ipkg
PKG_VERSION:=0.99.149
PKG_RELEASE:=ud1.2
PKG_MD5SUM:=975cc419d6db5fb279dc58177c68373b

PKG_SOURCE_URL:=http://www.handhelds.org/packages/ipkg \
	http://www.gtlib.gatech.edu/pub/handhelds.org/packages/ipkg \
	http://ftp.gwdg.de/pub/linux/handhelds/packages/ipkg
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_CAT:=zcat

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_INSTALL_DIR:=$(PKG_BUILD_DIR)/ipkg-install

include $(TOPDIR)/package/rules.mk

$(eval $(call PKG_template,IPKG_C,ipkg,$(PKG_VERSION)-$(PKG_RELEASE),$(ARCH)))
$(eval $(call PKG_template,IPKG_SH,ipkg-sh,$(PKG_VERSION)-$(PKG_RELEASE),$(ARCH)))

$(PKG_BUILD_DIR)/.configured:
	(cd $(PKG_BUILD_DIR); rm -rf config.{cache,status} ; \
		$(TARGET_CONFIGURE_OPTS) \
		CFLAGS="$(TARGET_CFLAGS)" \
		CPPFLAGS="-I$(STAGING_DIR)/usr/include" \
		LDFLAGS="-L$(STAGING_DIR)/usr/lib" \
		./configure \
		  --target=$(GNU_TARGET_NAME) \
		  --host=$(GNU_TARGET_NAME) \
		  --build=$(GNU_HOST_NAME) \
		  --program-prefix="" \
		  --program-suffix="" \
		  --prefix=/usr \
		  --exec-prefix=/usr \
		  --bindir=/bin \
		  --datadir=/usr/share \
		  --includedir=/usr/include \
		  --infodir=/usr/share/info \
		  --libdir=/usr/lib \
		  --libexecdir=/usr/lib \
		  --localstatedir=/var \
		  --mandir=/usr/share/man \
		  --sbindir=/usr/sbin \
		  --sysconfdir=/etc \
		  $(DISABLE_LARGEFILE) \
		  $(DISABLE_NLS) \
	)
	touch $@

$(PKG_BUILD_DIR)/.built:
	rm -rf $(PKG_INSTALL_DIR)
	mkdir -p $(PKG_INSTALL_DIR)
	$(MAKE) -C $(PKG_BUILD_DIR) \
		CC=$(TARGET_CC) \
		DESTDIR="$(PKG_INSTALL_DIR)" \
		all install
	touch $@

$(IPKG_IPKG_C):
	install -d -m0755 $(IDIR_IPKG_C)/bin
	cp -fpR $(PKG_INSTALL_DIR)/bin/ipkg-cl $(IDIR_IPKG_C)/bin/ipkg
	install -d -m0755 $(IDIR_IPKG_C)/usr/lib
	cp -fpR $(PKG_INSTALL_DIR)/usr/lib/libipkg.so.* $(IDIR_IPKG_C)/usr/lib/
	$(RSTRIP) $(IDIR_IPKG_C)
	$(IPKG_BUILD) $(IDIR_IPKG_C) $(PACKAGE_DIR)
	
$(IPKG_IPKG_SH):
	install -d -m0755 $(IDIR_IPKG_SH)/bin
	install -m0755 ./files/ipkg $(IDIR_IPKG_SH)/bin/ipkg
	$(IPKG_BUILD) $(IDIR_IPKG_SH) $(PACKAGE_DIR)
