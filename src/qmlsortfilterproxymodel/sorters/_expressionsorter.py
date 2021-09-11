from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QQmlScriptString, QQmlExpression, QQmlContext, qmlContext

from qmlsortfilterproxymodel.sorters._sorter import Sorter

def evaluateBoolExpression(expression):
    result = expression.evaluate()
    if expression.hasError():
        print(expression.error())
        return False
    try:
        return result[0]
    except:
        print("Cannot Convert result to bool", expression.sourceFile().toUtf8().data(), ":", expression.lineNumber(), ":", expression.columnNumber(), ":")
        return False

class ExpressionSorter(Sorter):
    expressionChanged = Signal()
    
    def __init__(self, parent: QObject = None):
        Sorter.__init__(self, parent=parent)
        
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
    def compare(self, sourceLeft, sourceRight, proxyModel):
        if self._scriptString.isEmpty():
            return 0
        else:
            roleNames = proxyModel.roleNames()

            modelLeftMap = {}
            modelRightMap = {}
            
            context = QQmlContext(qmlContext(self))
            
            for role in roleNames:
                roleName = roleNames[role]
                modelLeftMap[roleName] = proxyModel.sourceData(sourceLeft, role)
                modelRightMap[roleName] = proxyModel.sourceData(sourceRight, role)
                
            modelLeftMap["index"] = sourceLeft.row()            
            modelRightMap["index"] = sourceRight.row()            
            
            expression = QQmlExpression(self._scriptString, context)

            context.setContextProperty("modelLeft", modelLeftMap)
            context.setContextProperty("modelRight", modelRightMap)

            if (evaluateBoolExpression(expression)):
                    return -1

            context.setContextProperty("modelLeft", modelRightMap)
            context.setContextProperty("modelRight", modelLeftMap)

            if (evaluateBoolExpression(expression)):
                    return 1
            
            return 0

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
    