# OpenWrt One fork: dual-direction relay and native APK

This fork addresses the transport/recovery problems described in
[dy0422 issue #1](https://github.com/dy0422/ps5-portal-high-bitrate-openwrt/issues/1).
It does not establish PlayStation Portal 7.3.2 compatibility or measured bitrate.
The upstream project and its MIT license are retained.

## Changes

- Redirect both peers using **unicast** ARP replies at 5 Hz. No broadcast GARP
  and no periodic rewriting of the router's neighbor table.
- In the owned network namespace only, enable IPv4 forwarding and install an
  nftables table whose default is drop. Only PS5-to-Portal is kernel-forwarded;
  Portal-to-PS5 remains the single Python control/patch path.
- Validate the namespace inode and host/relay separation before permitting
  enabled forwarding. The host's global forwarding and firewall stay unchanged.
- Restore both peers on graceful shutdown and guardian recovery. Keep the
  supervisor's exclusive lock and resource-ownership checks.
- Retain code/config-bound baseline checks; a code or profile change requires
  a new baseline. Unlike the issue's workaround, do not skip verification.
- Add 35/45 profiles alongside 65/100/200, and allow 90 seconds for guardian
  cold start on small ARM devices. Start with 65 or lower, not 200.

Video now takes an extra hop through the namespace/kernel. It does **not** cross
the Python receive loop. This fork must not be described as a direct video path
or as having proven latency/throughput gains.

## Native APK

The **OpenWrt One APK** GitHub Actions workflow uses the official OpenWrt
**25.12.5 mediatek/filogic SDK** and its package machinery. It verifies the SDK
archive SHA256 and produces an APK, BUILDINFO, SDK configuration and SHA256SUMS.
The app is Python/scripts, so its package architecture is independent; native
dependencies (including kmod-veth) resolve from the installed firmware's feeds.
No kernel module or firmware image is bundled or flashed.

Download `portal-bitrate-openwrt-one-25.12.5-apk` from a successful Actions run.
Verify SHA256SUMS. This independently built APK is not signed by OpenWrt's
official feed key; do not treat it as an official OpenWrt package. A one-off
local installation can use `apk add --allow-untrusted ./portal-bitrate-*.apk`
after verifying its provenance/checksum. Do not disable feed signature checks.

Installation leaves the service disabled. LuCI: **Services → PS Portal 提码率**.
Choose a verified free LAN address outside the DHCP range for the namespace;
do not reuse the router's, PS5's or Portal's address. Complete `doctor`, enrollment,
unchanged baseline, then a bounded trial before enabling autostart. Baseline
also temporarily redirects ARP; it does not modify the bitrate payload.

The package was built for the pinned firmware family, not an arbitrary future
kernel. A different firmware must resolve matching kernel dependencies from its
own feeds. SDK build success does not prove real-console compatibility.

## Tests

- Protocol, baseline, dual-peer ARP repair, host-namespace rejection and LuCI/RPC
  unit tests run before the SDK job.
- Disposable OpenWrt network tests exercise actual veth/netns/nftables, packet
  mutation, kernel return forwarding, duplicate prevention, host-neighbor
  preservation, exclusive ownership, graceful stop and killed-engine recovery.
- These tests use synthetic endpoints, not Sony devices. Never run test fixtures
  on a home router: they replace test configuration and create simulated peers.

Both projects use the same recorded startup-packet heuristic. A modified-packet
counter alone is not proof of PS5 acceptance; verify picture and controls.
