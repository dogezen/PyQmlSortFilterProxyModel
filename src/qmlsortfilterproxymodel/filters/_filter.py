from PySide6.QtCore import QModelIndex, QObject, Signal, Slot, Property

class Filter(QObject):
    
    enabledChanged = Signal()
    invertedChanged = Signal()
    invalidated = Signal()
    
    def __init__(self, parent: QObject = None):
        QObject.__init__(self, parent=parent)
        
        self._enabled = True
        self._inverted = False
        
    @Property(bool, notify=enabledChanged)
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        if self._enabled == enabled:
            return
        self._enabled = enabled
        self.enabledChanged.emit()
        self.invalidated.emit()

    @Property(bool, notify=invertedChanged)
    def inverted(self):
        return self._inverted

    @inverted.setter
    def inverted(self, inverted):
        if self._inverted == inverted:
            return
        self._inverted = inverted
        self.invertedChanged.emit()
        self.invalidated.emit()
    
    def filterAcceptsRow(self, sourceIndex, proxyModel):
        return (not self._enabled) or (self.filterRow(sourceIndex, proxyModel) ^ self._inverted)

    # overridable
    @Slot()
    def invalidate(self):
        if self._enabled:
            self.invalidated.emit()
    
    # implement
    def filterRow(self, sourceIndex: QModelIndex, proxyModel):
        return True
    
    def proxyModelCompleted(self, proxyModel):
        pass
