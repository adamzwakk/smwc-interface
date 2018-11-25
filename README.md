# SMWC Interface

A python script that will read all the entries from Super Mario World Central (it caches all the available entries on first run), let you pick any hack to apply to your rom, and automatically apply the bps file to it (IPS planned next). Using this tool really speeds up the process of grabbing a certain hack and applying the patch for it.
### Features
- Lists all hacks from SMWC and caches the results for later use after first run
- Automatically downloads, unzips, and applies bps patches
- All output sfc files are saved and renamed to the hack title found on SMWC
### Planned Features
- IPS patching
- Update the cache/list from SMWC after X days
- Customizability, add options where to save, keep bps files or delete them
- Garbage collection, everything is stored in `/tmp` but could do better

Mostly made it so I could spin up a hack I already know and have it ready to go without using any external tools.