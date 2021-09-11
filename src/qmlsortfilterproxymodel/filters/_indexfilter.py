from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.filters._filter import Filter

class IndexFilter(Filter):
    minimumIndexChanged = Signal()
    maximumIndexChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        Filter.__init__(self, parent=parent)
        
        self._minimumIndex = None
        self._maximumIndex = None
    
    @Property("QVariant", notify=minimumIndexChanged)
    def minimumIndex(self):
        return self._minimumIndex
    
    @minimumIndex.setter
    def minimumIndex(self, minimumIndex):
        if self._minimumIndex == minimumIndex:
            return
        self._minimumIndex = minimumIndex
        self.minimumIndexChanged.emit()
        self.invalidate()

    @Property("QVariant", notify=maximumIndexChanged)
    def maximumIndex(self):
        return self._maximumIndex
    
    @maximumIndex.setter
    def maximumIndex(self, maximumIndex):
        if self._maximumIndex == maximumIndex:
            return
        self._maximumIndex = maximumIndex
        self.maximumIndexChanged.emit()
        self.invalidate()
        
    # override
    def filterRow(self, sourceIndex, proxyModel):
        sourceRowCount = proxyModel.sourceModel().rowCount()
        sourceRow = sourceIndex.row()
        
        try:
            minimum = int(self._minimumIndex)
            actualMinimum = minimum
            if minimum < 0:
                actualMinimum = sourceRowCount + minimum
            if sourceRow < actualMinimum:
                return False
        except Exception as err:
            pass

        try:
            maximum = int(self._maximumIndex)
            actualmaximum = maximum
            if maximum < 0:
                actualmaximum = sourceRowCount + maximum
            if sourceRow > actualmaximum:
                return False
        except Exception as err:
            pass
        
        return True
