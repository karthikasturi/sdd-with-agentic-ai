# "Spec" — Under-Specified

The entire requirement, as written by a real engineer trying to move fast:

> Alerts that aren't handled in a reasonable time should get escalated so nothing falls through the cracks.

That's the whole thing. No definition of "handled," no definition of "reasonable time," no definition of what "escalated" actually does, no statement of which severities this applies to, no statement of whether it can happen more than once per alert.

See `output-from-under-specified.py` for what an implementation attempt against this actually produces, and `../comparison.md` for the critique.
