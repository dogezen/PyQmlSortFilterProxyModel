from PySide6.QtCore import Qt, QObject, Signal, Slot, Property

class Sorter(QObject):
    
    enabledChanged = Signal()
    sortOrderChanged = Signal()
    priorityChanged = Signal()
    
    invalidated = Signal()
    
    
    def __init__(self, parent: QObject = None):
        QObject.__init__(self, parent=parent)
        
        self._enabled = True
        self._sortOrder = Qt.AscendingOrder
        self._priority = 0
        
    @Property(bool, notify=enabledChanged)
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, enabled):
        if self._enabled == enabled:
            return False
        
        self._enabled = enabled
        self.enabledChanged.emit()
        self.invalidated.emit()

    @Property(bool, notify=sortOrderChanged)
    def ascendingOrder(self):
        return self._sortOrder == Qt.AscendingOrder
    
    @ascendingOrder.setter
    def ascendingOrder(self, ascendingOrder):        
        if ascendingOrder:
            self.sortOrder = Qt.AscendingOrder
        else:
            self.sortOrder = Qt.DescendingOrder
        
    @Property(int, notify=sortOrderChanged)
    def sortOrder(self):
        return self._sortOrder
    
    @sortOrder.setter
    def sortOrder(self, sortOrder):        
        if self._sortOrder == sortOrder:
            return False
        
        self._sortOrder = sortOrder
        self.sortOrderChanged.emit()
        self.invalidated.emit()

    @Property(int, notify=priorityChanged)
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, priority):
        if self._priority == priority:
            return False
        
        self._priority = priority
        self.priorityChanged.emit()
        self.invalidated.emit()
        
    def compareRows(self, source_left, source_right, proxyModel):
        comparison = self.compare(source_left, source_right, proxyModel)
        if self._sortOrder == Qt.AscendingOrder:
            return comparison
        else:
            return -comparison
    
    def proxyModelCompleted(self, proxyModel):
        pass
    
    def compare(self, sourceLeft, sourceRight, proxyModel) -> int:
        if self.lessThan(sourceLeft, sourceRight, proxyModel):
            return -1
        if self.lessThan(sourceRight, sourceLeft, proxyModel):
            return 1
        return 0
    
    def lessThan(self, sourceLeft, sourceRight, proxyModel) -> bool:
        return False
    
    def invalidate(self):
        if self._enabled:
            self.invalidated.emit()
