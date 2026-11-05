#!/bin/zsh
# Read-only health check for an always-on Mac. It changes nothing.
# Run it on the machine, or from another computer:  ssh <user>@<machine-name> 'zsh -s' < health-check.sh
echo "== Machine"
hostname; uptime
echo
echo "== Your scheduled jobs (exit status 0 = last run was fine)"
for f in ~/Library/LaunchAgents/*.plist(N); do
  label=$(plutil -extract Label raw "$f" 2>/dev/null) || continue
  line=$(launchctl list | awk -v l="$label" '$3==l')
  every=$(plutil -extract StartInterval raw "$f" 2>/dev/null)
  out=$(plutil -extract StandardOutPath raw "$f" 2>/dev/null)
  last="-"; [[ -n "$out" && -e "$out" ]] && last=$(stat -f "%Sm" -t "%b %d %H:%M" "$out")
  printf "%-45s status=%-4s every=%-7s last log write: %s\n" "$label" "$(echo $line | awk '{print $2}')" "${every:+${every}s}${every:-other}" "$last"
done
echo
echo "== Sleep (want: sleep 0)"
pmset -g | grep -E "^ *(sleep|displaysleep|autorestart)"
echo
echo "== Automatic macOS update installs (want: 0)"
defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates 2>/dev/null || echo "not set (macOS default)"
echo
echo "== Disk"
df -h / | tail -1
