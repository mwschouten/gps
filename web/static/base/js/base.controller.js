
app.controller('TestCtrl', function($scope, $http) {
  init = function() {{}
  }

  init()
});


app.controller('LocationCtrl', function($scope, $http, $rootScope) {
    init = function(){
        $scope.name = 'Select a GPS station'

        $http.get("api/locations")
            .success(function(data){
                $scope.projects = data['projects']
            })

        $scope.treeOptions = {
          nodeChildren: "locations",
          dirSelectable: false,
        }
    }

    $scope.select = function (x) {
      console.log('Selected ' ,x)
      $rootScope.$broadcast('toggleStation',x)
      x.isloaded = !x.isloaded
    }


    init()
});




app.controller('chartctrl', function ($scope, $http) {

    stationids = []
    do_range = true

    convertDate = function(xx){ 
      return xx.map( 
        function (a){ 
          a[0] = Date.parse(a[0])
          return a
        })
    }


    $scope.$on('toggleStation', function (event, arg) { 
      var i = stationids.indexOf(arg.id)
      if (i > -1){
        console.log('Chart removes ',arg.name)
        stationids.splice(i,1)
        $scope.chartConfig.series.splice(i,1)
      }     
      else{
        console.log('Chart loads ',arg.name)
        loadSeries(arg)
      }
    })


    loadSeries = function(arg){
      console.log('Go load data for ',arg.name)
      $scope.chartConfig.loading = true
      $http({
              url:"api/series",
              method:'GET',
              params:{'id':arg.id,'ranges':do_range}
            })
           .success(function(data){

              $scope.chartConfig.loading = false
              $scope.chartConfig.series.push(
                {
                  data: convertDate(data['data']), name:arg.name
                }
              )
              if (do_range){
                $scope.chartConfig.series.push(
                  {
                    data: convertDate(data['ranges']), name:'Range',
                    type:'arearange',lineWidth:0,
                    fillOpacity: 0.3, zIndex:0
                  }
                )
              }

              stationids.push(arg.id)
              console.log($scope.chartConfig.series)
           })
    };


    $scope.toggleLoading = function () {
        this.chartConfig.loading = !this.chartConfig.loading
    }

    $scope.chartConfig = {
        options: {
            chart: {
                type: 'line',
                zoomType: 'xy'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Deformation [m]'
                }
            },
        },
        series: [],
        title: {
            text: ''
        },

        loading: false
    }
});



