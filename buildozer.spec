[app]

title = Todo Mobile
package.name = todomobile
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# Only python3 and kivy are listed here.
#
# Note: charset-normalizer is NOT listed but is still built. The Kivy recipe
# depends on requests, which pulls it in transitively. Listing it here (pinned
# or not) would not control it either: p4a strips the version and re-resolves
# the package in a separate step. The way to constrain it is the PIP_CONSTRAINT
# file the CI workflow writes.
#
# python3/hostpython3 are deliberately unpinned. The p4a recipe carries
# version-specific patches; forcing a CPython version the installed p4a was not
# written for is a classic source of opaque build failures.
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# --- Android -----------------------------------------------------------------

# Set explicitly so builds are reproducible rather than tracking whatever the
# installed buildozer happens to default to.
android.api = 35
android.minapi = 24
android.ndk_api = 24

# android.ndk is deliberately NOT pinned. The old "25b" pin was paired with an
# unpinned p4a, which is the mismatch that bites. Let buildozer choose the NDK
# that its p4a expects.

# Debug CI builds target one ABI to halve build time.
# For a Play Store release add: arm64-v8a, armeabi-v7a
android.archs = arm64-v8a

android.allow_backup = True

# Accept the SDK licence non-interactively. The licence prompt is interactive
# and will hang (or EOF-fail) a CI build without this.
android.accept_sdk_license = True

# "develop", NOT the v2026.05.09 tag. That release resolves charset-normalizer
# to its Android wheel, then installs it with host pip, which rejects it:
#   ERROR: charset_normalizer-...-android_24_arm64_v8a.whl
#          is not a supported wheel on this platform
# Fixed upstream in python-for-android#3366, which is on develop.
# This must match P4A_REF in .github/workflows/build-apk.yml.
p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1