from PySide6.QtCore import QObject, Signal, Slot, Property

from qmlsortfilterproxymodel.filters._filtercontainer import FilterContainer

class AllOfFilter(FilterContainer):
    roleNameChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        FilterContainer.__init__(self, parent=parent)
        
    def filterRow(self, sourceIndex, proxyModel):
        # return true if all filters return false, or if there is no filter.
        if len(self._filters) == 0:
            return True

        numEnabledFilters = 0
        numEnabledFiltersThatAcceptRows = 0
        for filter in self._filters:
            if filter.enabled:
                numEnabledFilters += 1
            if filter.enabled and filter.filterAcceptsRow(sourceIndex, proxyModel):
                numEnabledFiltersThatAcceptRows += 1
        acceptRow = (numEnabledFilters == numEnabledFiltersThatAcceptRows)
        return acceptRow