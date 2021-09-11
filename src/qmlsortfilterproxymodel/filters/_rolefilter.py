from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.filters._filter import Filter

class RoleFilter(Filter):
    roleNameChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        Filter.__init__(self, parent=parent)
        
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
        
    def sourceData(self, sourceIndex, proxyModel):
        data = proxyModel.sourceDataFromRoleName(sourceIndex, self._roleName)
        return data