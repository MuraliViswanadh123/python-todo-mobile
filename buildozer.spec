[app]

title = Todo Mobile
package.name = todomobile
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# Only what the app actually imports.
#
# Changes from the previous spec:
#   * dropped python3==3.11.5 / hostpython3==3.11.5. The p4a recipe carries
#     version-specific patches; forcing a CPython version the installed p4a
#     was not written for is a classic source of opaque build failures.
#     Buildozer 1.6 picks the Python version its p4a actually supports.
#   * dropped charset-normalizer. Nothing here imports it (it only arrives via
#     `requests`), and charset-normalizer >= 3 ships a C extension that needs a
#     p4a recipe, so a "<3.5" bound does not make it safe. If you ever do need
#     it, pin the last pure-Python release: charset-normalizer==2.1.1
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
# unpinned p4a, which is the mismatch that bites. The CI workflow pins p4a to a
# tag instead and lets buildozer choose the NDK that tag expects.

# Debug CI builds target one ABI to halve build time.
# For a Play Store release add: arm64-v8a, armeabi-v7a
android.archs = arm64-v8a

android.allow_backup = True

# Accept the SDK licence non-interactively. The licence prompt is interactive
# and will hang (or EOF-fail) a CI build without this.
android.accept_sdk_license = True

# Pin python-for-android to a release tag so an upstream commit cannot break
# main overnight. Keep this in step with BUILDOZER_VERSION in the workflow.
p4a.branch = v2026.05.09

[buildozer]

log_level = 2
warn_on_root = 1