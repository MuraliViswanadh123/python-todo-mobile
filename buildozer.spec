[app]
title = Todo Mobile
package.name = todomobile
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.11.5,hostpython3==3.11.5,kivy,charset-normalizer<3.5
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1