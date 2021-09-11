from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.filters._rolefilter import RoleFilter

class ValueFilter(RoleFilter):
    valueChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        RoleFilter.__init__(self, parent=parent)
        
        self._value = None
    
    @Property("QVariant", notify=valueChanged)
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if self._value == value:
            return
        self._value = value
        self.valueChanged.emit()
        self.invalidate()
        
    # override
    def filterRow(self, sourceIndex, proxyModel):
        return (self.value is None) or (self._value == self.sourceData(sourceIndex, proxyModel))