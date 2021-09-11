from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.filters._filtercontainer import FilterContainer

class AnyOfFilter(FilterContainer):
    roleNameChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        FilterContainer.__init__(self, parent=parent)
        
    def filterRow(self, sourceIndex, proxyModel):
        if len(self._filters) == 0:
            # return true if no filters
            return True
        # return true if any of the enabled filters return true
        for filter in self._filters:
            if filter.enabled and filter.filterAcceptsRow(sourceIndex, proxyModel):
                return True
        return False