from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.filters._rolefilter import RoleFilter

class RangeFilter(RoleFilter):
    minimumValueChanged = Signal()
    minimumInclusiveChanged = Signal()
    maximumValueChanged = Signal()
    maximumInclusiveChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        RoleFilter.__init__(self, parent=parent)
        
        self._minimumValue = None
        self._minimumInclusive = True
        self._maximumValue = None
        self._maximumInclusive = True
    
    @Property("QVariant", notify=minimumValueChanged)
    def minimumValue(self):
        return self._minimumValue
    
    @minimumValue.setter
    def minimumValue(self, minimumValue):
        if self._minimumValue == minimumValue:
            return
        self._minimumValue = minimumValue
        self.minimumValueChanged.emit()
        self.invalidate()

    @Property(bool, notify=minimumInclusiveChanged)
    def minimumInclusive(self):
        return self._minimumInclusive
    
    @minimumInclusive.setter
    def minimumInclusive(self, minimumInclusive):
        if self._minimumInclusive == minimumInclusive:
            return
        self._minimumInclusive = minimumInclusive
        self.minimumInclusiveChanged.emit()
        self.invalidate()

    @Property("QVariant", notify=maximumValueChanged)
    def maximumValue(self):
        return self._maximumValue
    
    @maximumValue.setter
    def maximumValue(self, maximumValue):
        if self._maximumValue == maximumValue:
            return
        self._maximumValue = maximumValue
        self.maximumValueChanged.emit()
        self.invalidate()
        
    @Property(bool, notify=maximumInclusiveChanged)
    def maximumInclusive(self):
        return self._maximumInclusive
    
    @maximumInclusive.setter
    def maximumInclusive(self, maximumInclusive):
        if self._maximumInclusive == maximumInclusive:
            return
        self._maximumInclusive = maximumInclusive
        self.maximumInclusiveChanged.emit()
        self.invalidate()
        
    # override
    def filterRow(self, sourceIndex, proxyModel):
        value = self.sourceData(sourceIndex, proxyModel)

        lessThanMin = (self._minimumValue is not None)
        if self._minimumInclusive:
            lessThanMin = lessThanMin and (value < self._minimumValue) 
        else:
            lessThanMin = lessThanMin and (value <= self._minimumValue) 

        moreThanMax = (self._maximumValue is not None)
        if self._maximumInclusive:
            moreThanMax = moreThanMax and (value > self._maximumValue) 
        else:
            moreThanMax = moreThanMax and (value >= self._maximumValue) 
                       
        return not (lessThanMin or moreThanMax)
