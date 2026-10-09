"""Puts the repository root on sys.path so the integrated pipeline modules
import by name under pytest, regardless of the directory pytest is run from.

The four integrated modules live at the repository root rather than in a
package, which is how they were preserved. This file is the whole of the
import wiring the suite needs; there is no build step.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
