# PyQmlSortFilterProxyModel
This project is a python PySide6 port of [https://github.com/oKcerG/SortFilterProxyModel](https://github.com/oKcerG/SortFilterProxyModel); a QSortFilterProxyModel exposed to QML written by oKcerG.

Please refer to oKcerG's documentation for usage as much of this implementation is based on oKcerG's implementation.

## Components not (yet) ported

- `ProxyRoles`
- `QQmlSortFilterProxyModel::componentCompleted`. In PySide6, there is no `Q_INTERFACES` macro enabling a class to inherits from `QSortFilterProxyModel` and `QQmlParserStatus`. Hence inheriting from `QQmlParserStatus` doesn't cause errors, however the `componentCompleted` method is not called.
- Some of the sorters are not yet ported
- The `delay` functionality is not ported
- Attached properties not ported

## Differences - Container Filters

Because attached properties are not ported, there is a difference in using the `AnyOf` and `AllOf` filters:

```qml

// oKcerG's
AnyOf {
    RoleFilter {...}
    RegExpFilter {...}
    //...
}

// python implementation
AnyOf {
    // need to assign a list of Filter to the filters property
    filters: [
        RoleFilter {...},
        RegExpFilter {...},
        //...
    ]
}

```

# Usage

1. download /clone the repostitory
2. copy `src/qmlsortfilterproxymodel` to your project
3. import and register the `SortFilterProxyModel` to `qml`

```python

# main.py
import qmlsortfilterproxymodel
# register qml types before QQmlApplicationEngine.load("main.qml") is called
qmlsortfilterproxymodel.registerQmlTypes()
```

4. Instantiate `SortFilterProxyModel` in `qml`

```qml
// SomeFile.qml
import SortFilterProxyModel 0.2


SortFilterProxyModel {
    //...
}

```

# Running the Example

1. Create a virtual environment (currently `venv` folder is under `.gitignore`) and activate
    `python3 -m venv venv`
    `source venv/bin/activate`
2. Install requirements (`PySide6`)
    `pip3 install -r requirements.txt`
3. Run the example project
    `python3 example/main.py`

Once the example window launches, you can use the `TextField` to filter by name.
