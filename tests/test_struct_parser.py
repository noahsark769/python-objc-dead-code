from unittest import TestCase

from parsers.struct import parse

class EnumSymbolParserTest(TestCase):
    def test_structs(self):
        content = """
        // Options for displaying localized distances
        typedef struct {
          unsigned int appendUnits : 1;               // If YES, append units
          unsigned int leadingZero : 1;               // If YES, allow leading zero (0.3 instead of .3)
          unsigned int newlineSeparatorNonMetric : 1; // If YES, add newline in between value and units (Non-metric only)
          unsigned int unicodeFractions : 1;          // If YES, show unicode fractions
          unsigned int useLabels : 1;
          unsigned int hideZero : 1;        // If YES and the value evaluates to 0, then return empty string
          unsigned int abbreviateUnits : 1; // If YES use unit abbreviations (i.e. miles -> mi)
        } YPLocalizationDistanceOptions;
        """
        self.assertItemsEqual(
            [
            "YPLocalizationDistanceOptions",
            "appendUnits",
            "leadingZero",
            "newlineSeparatorNonMetric",
            "unicodeFractions",
            "useLabels",
            "hideZero",
            "abbreviateUnits",
            ],
            parse(content)
        )
