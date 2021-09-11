from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import ListProperty

from qmlsortfilterproxymodel.filters._filter import Filter

class FilterContainer(Filter):
    roleNameChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        Filter.__init__(self, parent=parent)
        
        # filters
        self._filters = []

    # START FILTERS PROPERTY IMPLEMENTATION
    def _append_filter(self, filter: Filter):
        filter.setParent(self)
        self._filters.append(filter)
        filter.invalidated.connect(self.invalidate)
        self.invalidate()
                
    def _at_filter(self, index):
        return self._filters[index]
        
    def _clear_filters(self):
        self._filters = []
        self.invalidate()
        
    def _count_filters(self):
        return len(self._filters)

    filters = ListProperty(Filter, _append_filter, _at_filter, _clear_filters, _count_filters) 
    # END FILTERS PROPERTY IMPLEMENTATION
