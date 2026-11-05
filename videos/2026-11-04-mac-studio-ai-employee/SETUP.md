# Set up an always-on Mac in four steps

1. **Install Tailscale** on every computer (https://tailscale.com). Approve the VPN prompt your Mac shows you.
2. **Sign in with the same account** on each one. Your devices now share a private network that only your account can see. Nothing is opened to the public internet.
3. **On the computer you want to reach:** System Settings > General > Sharing. Turn on **Screen Sharing**, **Remote Login**, or both. Click the (i) next to each and allow access for **your own user only**.
4. **Connect by the machine's name.**
   - Desktop: open the Screen Sharing app and type the name.
   - Commands: `ssh <your-user>@<machine-name>`
   - For an AI agent, give it its **own login key** instead of your password:
     ```bash
     ssh-keygen -t ed25519 -f ~/.ssh/agent_key -C "agent"
     ssh-copy-id -i ~/.ssh/agent_key.pub <your-user>@<machine-name>
     ```

## Before you trust it to stay on

- **Turn off sleep:** System Settings > Energy > "Prevent automatic sleeping when the display is off" (on a laptop: Battery > Options).
  Or in Terminal: `sudo pmset -a sleep 0` (you type the password, not your agent).
- **Turn off automatic update installs:** System Settings > General > Software Update > Automatic Updates (i) > turn off "Install macOS updates".
  An update can restart the Mac and leave it waiting at the login screen.
