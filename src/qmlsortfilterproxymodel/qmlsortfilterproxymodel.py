
from typing import Dict

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QObject, Signal, Slot, Property
from PySide6.QtQml import ListProperty, QQmlParserStatus

from qmlsortfilterproxymodel.filters._filter import Filter
from qmlsortfilterproxymodel.sorters._sorter import Sorter

class QmlSortFilterProxyModel(QSortFilterProxyModel):
    
    # signals
    countChanged = Signal()
    sortRoleNameChanged = Signal()
    ascendingSortOrderChanged = Signal()

    filterRoleNameChanged = Signal()
    filterRoleValueChanged = Signal()    
    filterPatternChanged = Signal()

    def __init__(self, parent: QObject = None):
        QSortFilterProxyModel.__init__(self, parent=parent)
        
        self.rowsInserted.connect(self.countChanged)
        self.rowsRemoved.connect(self.countChanged)
        self.modelReset.connect(self.countChanged)
        self.layoutChanged.connect(self.countChanged)
        
        self._ascendingSortOrder = True
        self._sortRoleName = ''
        
        self._filterRoleName = ''
        self._filterRoleValue = None
        
        # filters
        self._filters = []
        
        # sorters
        self._sorters = []
        
        self.setDynamicSortFilter(True)
        self.sort(0)

    @Property(int, notify=countChanged)
    def count(self):
        return self.rowCount()
    
    # START FILTERS PROPERTY IMPLEMENTATION
    def _append_filter(self, filter: Filter):
        filter.setParent(self)
        self._filters.append(filter)
        filter.invalidated.connect(self.invalidateFilter)
        
    def _at_filter(self, index):
        return self._filters[index]
        
    def _clear_filters(self):
        self._filters = []
        self.invalidateFilter()
        
    def _count_filters(self):
        return len(self._filters)

    filters = ListProperty(Filter, _append_filter, _at_filter, _clear_filters, _count_filters) 
    # END FILTERS PROPERTY IMPLEMENTATION

    # START sorters PROPERTY IMPLEMENTATION
    def _append_sorter(self, sorter: Sorter):
        sorter.setParent(self)
        self._sorters.append(sorter)
        sorter.invalidated.connect(self.invalidate)
        
    def _at_sorter(self, index):
        return self._sorters[index]
        
    def _clear_sorters(self):
        self._sorters = []
        self.invalidate()
        
    def _count_sorters(self):
        return len(self._sorters)

    sorters = ListProperty(Sorter, _append_sorter, _at_sorter, _clear_sorters, _count_sorters) 
    # END FILTERS PROPERTY IMPLEMENTATION
    
    @Property(str, notify=sortRoleNameChanged)
    def sortRoleName(self):
        return self._sortRoleName

    @sortRoleName.setter
    def sortRoleName(self, sortRoleName):
        if self._sortRoleName == sortRoleName:
            return
        self._sortRoleName = sortRoleName
        self._updateSortRole() # calls invalidate
        self.sortRoleNameChanged.emit()
        
    @Property(bool, notify=ascendingSortOrderChanged)
    def ascendingSortOrder(self):
        return self._ascendingSortOrder

    @ascendingSortOrder.setter
    def ascendingSortOrder(self, ascendingSortOrder):
        if self._ascendingSortOrder == ascendingSortOrder:
            return
        self._ascendingSortOrder = ascendingSortOrder
        self.ascendingSortOrderChanged.emit()
        self.invalidate()
        
    @Property(str, notify=filterRoleNameChanged)
    def filterRoleName(self):
        return self._filterRoleName

    @filterRoleName.setter
    def filterRoleName(self, filterRoleName):
        if self._filterRoleName == filterRoleName:
            return
        self._filterRoleName = filterRoleName
        self._updateFilterRole()
        self.filterRoleNameChanged.emit()        

    @Property("QVariant", notify=filterRoleValueChanged)
    def filterRoleValue(self):
        return self._filterRoleValue

    @filterRoleValue.setter
    def filterRoleValue(self, filterRoleValue):
        if self._filterRoleValue == filterRoleValue:
            return
        self._filterRoleValue = filterRoleValue
        self.filterRoleValueChanged.emit()
        self.invalidateFilter()

    @Property(str, notify=filterPatternChanged)
    def filterPattern(self):
        return self.filterRegularExpression().pattern()

    @filterPattern.setter
    def filterPattern(self, filterPattern):
        regex = self.filterRegularExpression()
        if regex.pattern() == filterPattern:
            return
        regex.setPattern(filterPattern)
        super().setFilterRegularExpression(regex) 
        self.filterPatternChanged.emit()    

    def sourceDataFromRoleName(self, sourceIndex: QModelIndex, roleName: str):
        role = self.roleForName(roleName)
        return self.sourceData(sourceIndex, role)

    def sourceData(self, sourceIndex: QModelIndex, role: int):
        return self.sourceModel().data(sourceIndex, role)

    @Slot(int, result="QVariantMap")
    def get(self, row):
        '''
            Return the item at row in the proxy model as a map of all its roles. This allows the item data to be read (not modified) from JavaScript.
        '''
        data = {}
        modelIndex = self.index(row, 0)
        roles = self.roleNames()
        for role in roles:
            roleName = str(roles[role], 'utf-8')
            data[roleName] = self.data(modelIndex, role)
        return data
    
    @Slot(int, str, result="QVariant")
    def getRoleValue(self, row, roleName):
        '''
            Return the data for the given roleName of the item at row in the proxy model. This allows the role data to be read (not modified) from JavaScript.
            This equivalent to calling {data(index(row, 0), roleForName(roleName))}.
        '''
        return self.data(self.index(row, 0), self.roleForName(roleName))

    @Slot(str, result=int)
    def roleForName(self, roleName):
        '''
            Returns the role number for the given roleName.
            If no role is found for this roleName, -1 is returned.
        '''
        names = self.roleNames()
        for role in names:
            if str(names[role], 'utf-8') == roleName:
                return role
        return -1
    
    # override: QSortFilterProxyModel::setSourceModel
    def setSourceModel(self, sourceModel):
        super().setSourceModel(sourceModel)
        self._updateSortRole()
        self._updateFilterRole()
    
    # override: QSortFilterProxyModel::roleNames
    def roleNames(self) -> Dict[int, bytes]:
        if self.sourceModel() != None:
            return self.sourceModel().roleNames()
        return {}
    
    # override: QSortFilterProxyModel::filterAcceptsRow
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        sourceIndex = self.sourceModel().index(source_row, 0, source_parent)
        # bool valueAccepted = !m_filterValue.isValid() || ( m_filterValue == sourceModel()->data(sourceIndex, filterRole()) );
        valueAccepted = True
        if self._filterRoleValue is not None:
            valueAccepted = (self._filterRoleValue == self.sourceModel().data(sourceIndex, self.filterRole()))
        baseAcceptsRow = valueAccepted and super().filterAcceptsRow(source_row, source_parent)
        for filter in self._filters:
            filterAcceptsRow = filter.filterAcceptsRow(sourceIndex, self)
            baseAcceptsRow = baseAcceptsRow and filterAcceptsRow
            if filterAcceptsRow == False:
                break
        return baseAcceptsRow
    
    # override: QSortFilterProxyModel::lessThan
    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        if len(self._sortRoleName) > 0:
            if super().lessThan(source_left, source_right):
                return self._ascendingSortOrder
            if super().lessThan(source_right, source_left):
                return not self._ascendingSortOrder

        # sort sorters by priority
        sortedSorters = sorted(self._sorters, key = lambda sorter: sorter.priority, reverse=True)
        for sorter in sortedSorters:
            if sorter.enabled:
                comparison = sorter.compareRows(source_left, source_right, self)
                if comparison != 0:
                    return comparison < 0
        return source_left.row() < source_right.row()
    
    # called whenever we update the sort role name
    # or a model is set
    def _updateSortRole(self):
        names = self.roleNames()
        for role in names:
            roleName = str(names[role], 'utf-8')
            if self._sortRoleName == roleName:
                self.setSortRole(role)
                self.invalidate()
                break
        
    def _updateFilterRole(self):
        names = self.roleNames()
        for role in names:
            roleName = str(names[role], 'utf-8')
            if self._filterRoleName == roleName:
                self.setFilterRole(role)
                self.invalidate()
                break
