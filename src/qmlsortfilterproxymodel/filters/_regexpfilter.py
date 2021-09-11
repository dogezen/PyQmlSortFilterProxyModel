
from PySide6.QtCore import QRegularExpressionMatch, Qt, QRegularExpression, QObject, Signal, Property, QEnum

from qmlsortfilterproxymodel.filters._rolefilter import RoleFilter

class RegExpFilter(RoleFilter):
    patternChanged = Signal()
    caseSensitivityChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        RoleFilter.__init__(self, parent=parent)
        
        self._pattern = ''
        self._caseSensitivity = Qt.CaseInsensitive
        self._regularExpression = QRegularExpression()
    
    @Property(str, notify=patternChanged)
    def pattern(self):
        return self._pattern
    
    @pattern.setter
    def pattern(self, pattern):
        if self._pattern == pattern:
            return
        self._pattern = pattern
        self._regularExpression.setPattern(self._pattern)
        self.patternChanged.emit()
        self.invalidate()
        
    @Property(int, notify=caseSensitivityChanged)
    def caseSensitivity(self):
        return self._caseSensitivity
    
    @caseSensitivity.setter
    def caseSensitivity(self, caseSensitivity):
        if self._caseSensitivity == caseSensitivity:
            return
        self._caseSensitivity = caseSensitivity
        
        options = self._regularExpression.patternOptions()
        if self._caseSensitivity == Qt.CaseInsensitive:
            options = options ^ 1
        else:
            options = options ^ 0
        self._regularExpression.setPatternOptions(options)
        
        self.caseSensitivityChanged.emit()
        self.invalidate()
        
    # override
    def filterRow(self, sourceIndex, proxyModel):
        try:
            string = str(self.sourceData(sourceIndex, proxyModel))
            match = self._regularExpression.match(string)
            return match.hasMatch()
        except Exception as err:
            return True