// tree.controller.js

app.controller('TreelistController', function ($scope) {
  
    $scope.current = 'aap'
    $scope.treeOptions = {
        nodeChildren: "children",
        dirSelectable: false,
        // injectClasses: {
        //     ul: "a1",
        //     li: "a2",
        //     liSelected: "a7",
        //     iExpanded: "a3",
        //     iCollapsed: "a4",
        //     iLeaf: "a5",
        //     label: "a6",
        //     labelSelected: "a8"
        // }
    }

});