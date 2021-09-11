from PySide6.QtQml import qmlRegisterType, qmlRegisterUncreatableType

from qmlsortfilterproxymodel.qmlsortfilterproxymodel import QmlSortFilterProxyModel
# filters
from qmlsortfilterproxymodel.filters._filter import Filter
from qmlsortfilterproxymodel.filters._valuefilter import ValueFilter
from qmlsortfilterproxymodel.filters._anyoffilter import AnyOfFilter
from qmlsortfilterproxymodel.filters._alloffilter import AllOfFilter
from qmlsortfilterproxymodel.filters._expressionfilter import ExpressionFilter
from qmlsortfilterproxymodel.filters._indexfilter import IndexFilter
from qmlsortfilterproxymodel.filters._rangefilter import RangeFilter
from qmlsortfilterproxymodel.filters._regexpfilter import RegExpFilter

# sorters
from qmlsortfilterproxymodel.sorters._rolesorter import RoleSorter
from qmlsortfilterproxymodel.sorters._expressionsorter import ExpressionSorter


def registerQmlTypes():
    qmlRegisterType(QmlSortFilterProxyModel, "SortFilterProxyModel", 1, 0, "SortFilterProxyModel")
    # filters
    qmlRegisterUncreatableType(Filter, "SortFilterProxyModel", 1, 0, "Filter", "Filter is abstract class")
    qmlRegisterType(ValueFilter, "SortFilterProxyModel", 1, 0, "ValueFilter")
    qmlRegisterType(AnyOfFilter, "SortFilterProxyModel", 1, 0, "AnyOf")
    qmlRegisterType(AllOfFilter, "SortFilterProxyModel", 1, 0, "AllOf")
    qmlRegisterType(ExpressionFilter, "SortFilterProxyModel", 1, 0, "ExpressionFilter")
    qmlRegisterType(IndexFilter, "SortFilterProxyModel", 1, 0, "IndexFilter")
    qmlRegisterType(RangeFilter, "SortFilterProxyModel", 1, 0, "RangeFilter")
    qmlRegisterType(RegExpFilter, "SortFilterProxyModel", 1, 0, "RegExpFilter")
    # sorters
    qmlRegisterType(RoleSorter, "SortFilterProxyModel", 1, 0, "RoleSorter")
    qmlRegisterType(ExpressionSorter, "SortFilterProxyModel", 1, 0, "ExpressionSorter")
