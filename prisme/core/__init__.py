"""
prisme Core Module
Translation Hub architecture components
"""

# Version
__version__ = "3.0.0"  # Translation Hub architecture

# Core exports
from .translation import TranslationPipeline
from .layers import TranslationLayer, ScaleQuantizeLayer, ArpeggiatorLayer

__all__ = [
    'TranslationPipeline',
    'TranslationLayer',
    'ScaleQuantizeLayer',
    'ArpeggiatorLayer',
]
