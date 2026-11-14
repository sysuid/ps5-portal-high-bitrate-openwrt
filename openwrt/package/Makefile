include $(TOPDIR)/rules.mk

PKG_NAME:=portal-bitrate
PKG_VERSION:=0.3.0
PKG_RELEASE:=1
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=sysuid
PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/portal-bitrate
  SECTION:=net
  CATEGORY:=Network
  TITLE:=PS Portal bitrate relay and LuCI management
  URL:=https://github.com/sysuid/ps5-portal-high-bitrate-openwrt
  DEPENDS:=+python3 +scapy +ip-full +kmod-veth +libpcap +luci-base +rpcd +nftables-json
endef

define Package/portal-bitrate/description
  Experimental dual-direction ARP relay in an owned network namespace.
  Control packets are patched in Python; return traffic uses the kernel.
  Includes LuCI settings. Installed disabled; baseline verification required.
endef

define Package/portal-bitrate/conffiles
/etc/config/portal_bitrate
endef

define Build/Prepare
	$(CP) ./src/. $(PKG_BUILD_DIR)/
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/portal-bitrate/install
	$(INSTALL_DIR) $(1)/usr/lib/portal-bitrate $(1)/usr/sbin $(1)/etc/init.d $(1)/etc/config
	$(CP) $(PKG_BUILD_DIR)/release-assets/root/usr/lib/portal-bitrate/. $(1)/usr/lib/portal-bitrate/
	chmod 0700 $(1)/usr/lib/portal-bitrate
	chmod 0600 $(1)/usr/lib/portal-bitrate/*
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/openwrt/files/portal-bitrate $(1)/usr/sbin/portal-bitrate
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/openwrt/files/portal-bitrate.init $(1)/etc/init.d/portal-bitrate
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/openwrt/files/portal_bitrate $(1)/etc/config/portal_bitrate
	$(CP) $(PKG_BUILD_DIR)/openwrt/luci/root/. $(1)/
	$(INSTALL_DIR) $(1)/www
	$(CP) $(PKG_BUILD_DIR)/openwrt/luci/htdocs/. $(1)/www/
	chmod 0755 $(1)/usr/libexec/rpcd/portal-bitrate
endef

define Package/portal-bitrate/preinst
#!/bin/sh
[ -n "$$IPKG_INSTROOT" ] && exit 0
if [ -x /usr/sbin/portal-bitrate ]; then
  apk info -e portal-bitrate >/dev/null 2>&1 || { echo 'Uninstall the script/other installation first.' >&2; exit 1; }
  /etc/init.d/portal-bitrate stop || exit 1
  /usr/sbin/portal-bitrate repair || exit 1
fi
[ ! -e /var/run/netns/portal-bitrate ] && [ ! -e /var/run/portal-lab-capture.lock ] || exit 1
exit 0
endef

define Package/portal-bitrate/postinst
#!/bin/sh
[ -n "$$IPKG_INSTROOT" ] && exit 0
uci set portal_bitrate.main.enabled=0
uci commit portal_bitrate
/etc/init.d/portal-bitrate disable
rm -f /tmp/luci-indexcache*
if /etc/init.d/rpcd running >/dev/null 2>&1; then /etc/init.d/rpcd reload; fi
exit 0
endef

define Package/portal-bitrate/prerm
#!/bin/sh
[ -n "$$IPKG_INSTROOT" ] && exit 0
/etc/init.d/portal-bitrate stop || exit 1
/usr/sbin/portal-bitrate repair || exit 1
/etc/init.d/portal-bitrate disable
exit 0
endef

define Package/portal-bitrate/postrm
#!/bin/sh
[ -n "$$IPKG_INSTROOT" ] && exit 0
[ ! -e /var/run/netns/portal-bitrate ] || exit 1
rm -rf /usr/lib/portal-bitrate/__pycache__
rm -f /tmp/luci-indexcache*
if /etc/init.d/rpcd running >/dev/null 2>&1; then /etc/init.d/rpcd reload; fi
exit 0
endef

$(eval $(call BuildPackage,portal-bitrate))
