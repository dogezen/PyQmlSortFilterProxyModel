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
    qmlRegisterType(QmlSortFilterProxyModel, "SortFilterProxyModel", 0, 2, "SortFilterProxyModel")
    # filters
    qmlRegisterUncreatableType(Filter, "SortFilterProxyModel", 0, 2, "Filter", "Filter is abstract class")
    qmlRegisterType(ValueFilter, "SortFilterProxyModel", 0, 2, "ValueFilter")
    qmlRegisterType(AnyOfFilter, "SortFilterProxyModel", 0, 2, "AnyOf")
    qmlRegisterType(AllOfFilter, "SortFilterProxyModel", 0, 2, "AllOf")
    qmlRegisterType(ExpressionFilter, "SortFilterProxyModel", 0, 2, "ExpressionFilter")
    qmlRegisterType(IndexFilter, "SortFilterProxyModel", 0, 2, "IndexFilter")
    qmlRegisterType(RangeFilter, "SortFilterProxyModel", 0, 2, "RangeFilter")
    qmlRegisterType(RegExpFilter, "SortFilterProxyModel", 0, 2, "RegExpFilter")
    # sorters
    qmlRegisterType(RoleSorter, "SortFilterProxyModel", 0, 2, "RoleSorter")
    qmlRegisterType(ExpressionSorter, "SortFilterProxyModel", 0, 2, "ExpressionSorter")
