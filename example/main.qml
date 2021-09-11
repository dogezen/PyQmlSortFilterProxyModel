import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.12
import QtQuick.Window 2.12

import SortFilterProxyModel 1.0

ApplicationWindow {
    id: root
    visible: true
    width: Screen.width * 0.95
    height: Screen.height * 0.8

    title: qsTr("Python SortFilterProxyModel Demo APP")
    
    flags: Qt.Window | Qt.WindowFullscreenButtonHint |
            Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint |
            Qt.WindowCloseButtonHint

    Component.onCompleted: {
        root.setX(Screen.width / 2.0 - root.width / 2.0)
        root.setY(Screen.height / 2.0 - root.height / 2.0)
        root.requestActivate()
        root.raise()
    }

    ListModel {
        id: dataModel
        ListElement {name: "Annie"; age: 22}
        ListElement {name: "James"; age: 45}
        ListElement {name: "George"; age: 18}
        ListElement {name: "Lisa"; age: 10}
        ListElement {name: "Laura"; age: 39}
    }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {

            Layout.fillWidth: true

            TextField {
                id: txtFilterName
                Layout.preferredWidth: 220
                placeholderText: "Filter name..."
            }

            Text {
                text: "Filtering: '" + txtFilterName.text + "'"
            }

            Item {
                Layout.fillWidth: true
            }
        }
        
        SortFilterProxyModel {
            id: proxyModel
            sourceModel: dataModel
            filters: [
                RegExpFilter {
                    roleName: "name"
                    pattern: txtFilterName.text
                    enabled: txtFilterName.text.length > 0
                }
            ]
        }

        ListView {
            id: lv

            clip: true

            Layout.fillWidth: true
            Layout.fillHeight: true

            model: proxyModel
            delegate: Rectangle {
                width: lv.width
                height: 30

                RowLayout {
                    anchors.fill: parent

                    Text {                    
                        text: name
                        Layout.leftMargin: 10
                        Layout.preferredWidth: 80
                    }

                    Text {                    
                        text: age
                        Layout.preferredWidth: 80
                    }

                    Item {Layout.fillWidth: true}
                }
            }
        }
    }
}
