#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${ANDROID_HOME:?Set ANDROID_HOME to Android SDK directory}"
: "${JAVA_HOME:?Set JAVA_HOME to JDK 17 directory}"
BT="$ANDROID_HOME/build-tools/35.0.0"
JAR="$ANDROID_HOME/platforms/android-35/android.jar"
mkdir -p build/classes build/dex build/res
"$JAVA_HOME/bin/javac" --release 8 -classpath "$JAR" -d build/classes MainActivity.java
"$JAVA_HOME/bin/jar" cf build/classes.jar -C build/classes .
"$BT/d8" --lib "$JAR" --output build/dex build/classes.jar
"$BT/aapt" package -f -M AndroidManifest.xml -S build/res -I "$JAR" -F build/unsigned.apk
(cd build/dex && zip -q ../unsigned.apk classes.dex)
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk
if [ ! -f build/debug.keystore ]; then
 "$JAVA_HOME/bin/keytool" -genkeypair -keystore build/debug.keystore -storepass android -keypass android -alias androiddebugkey -dname 'CN=Android Debug' -keyalg RSA -validity 3650
fi
"$BT/apksigner" sign --ks build/debug.keystore --ks-pass pass:android --out lab-notes.apk build/aligned.apk
"$BT/apksigner" verify lab-notes.apk
