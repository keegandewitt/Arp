"""
Boot configuration for Arp
Settings are now stored in NVM (microcontroller.nvm) which is always writable,
so we don't need to remount the filesystem anymore.
"""

# No filesystem remounting needed - using NVM for settings
print("Boot: Using NVM for settings persistence (filesystem remains writable from computer)")
