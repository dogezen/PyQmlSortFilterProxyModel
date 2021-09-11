from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.sorters._sorter import Sorter

class RoleSorter(Sorter):
    roleNameChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        Sorter.__init__(self, parent=parent)
        
        self._roleName = ''
    
    @Property(str, notify=roleNameChanged)
    def roleName(self):
        return self._roleName
    
    @roleName.setter
    def roleName(self, roleName):
        if self._roleName == roleName:
            return
        self._roleName = roleName
        self.roleNameChanged.emit()
        self.invalidate()
        
    def sourceData(self, sourceLeft, sourceRight, proxyModel):
        pair = (None, None)
        
        role = proxyModel.roleForName(self._roleName)
        
        if role == -1:
            return (None, None)

        leftValue = proxyModel.sourceData(sourceLeft, role)
        rightValue = proxyModel.sourceData(sourceRight, role)
                
        return (leftValue, rightValue)

    def compare(self, sourceLeft, sourceRight, proxyModel):
        leftValue, rightValue = self.sourceData(sourceLeft, sourceRight, proxyModel)
        if leftValue < rightValue:
            return -1
        if leftValue > rightValue:
            return 1
        return 0