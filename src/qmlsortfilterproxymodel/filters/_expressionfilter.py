from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QQmlScriptString, QQmlExpression, QQmlContext, qmlContext

from qmlsortfilterproxymodel.filters._filter import Filter

def addToContext(context, modelMap, name, value):
    context.setContextProperty(name, value)
    modelMap[name] = value

class ExpressionFilter(Filter):
    expressionChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        Filter.__init__(self, parent=parent)
        
        self._scriptString = QQmlScriptString()
        self._expression = None
        self._context = None
    
    @Property(QQmlScriptString, notify=expressionChanged)
    def expression(self):
        return self._scriptString
    
    @expression.setter
    def expression(self, scriptString):
        if self._scriptString == scriptString:
            return
        self._scriptString = scriptString
        
        self._updateExpression()
        
        self.expressionChanged.emit()
        self.invalidate()
        
    # override
    def filterRow(self, sourceIndex, proxyModel):
        if self._scriptString.isEmpty():
            return True
        else:
            modelMap = {}
            
            context = QQmlContext(qmlContext(self))
            
            roleNames = proxyModel.roleNames()
            for role in roleNames:
                roleName = roleNames[role].decode('utf-8')
                sourceData = proxyModel.sourceDataFromRoleName(sourceIndex, roleName)
                addToContext(context, modelMap, roleName, sourceData)
            addToContext(context, modelMap, "index", sourceIndex.row())
            
            context.setContextProperty("model", modelMap)
            
            expression = QQmlExpression(self._scriptString, context)
            result = expression.evaluate()
            if expression.hasError():
                print(expression.error())
                return True
            try:
                return result[0]
            except Exception as err:
                #if type(result) == type(True):
                #    return result
                #else:
                print("Cannot Convert result to bool", expression.sourceFile().toUtf8().data(), ":", expression.lineNumber(), ":", expression.columnNumber(), ":")
                return True

    def proxyModelCompleted(self, proxyModel):
        self._updateContext(proxyModel)

    def _updateContext(self, proxyModel):
        del self._context
        self._context = QQmlContext(qmlContext(self), self)
        
        modelMap = {}
        
        roleNames = proxyModel.roleNames()
        for roleName in roleNames:
            addToContext(self._context, modelMap, roleName, None)
        
        addToContext(self._context, modelMap, "index", -1)
        self._context.setContextProperty("model", modelMap)
        self._updateExpression()
            
    def _updateExpression(self):
        if self._context == None:
            return

        del self._expression
        self._expression = QQmlExpression(self._scriptString, self._context, 0, self)
        self._expression.valueChanged.connect(self.invalidate)
        self._expression.setNotifyOnValueChanged(True)
        self._expression.evaluate()
    