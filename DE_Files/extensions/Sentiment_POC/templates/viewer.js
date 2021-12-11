var token = "";
var tuid = "";
var ebs = "";

document.cookie = "flavor=choco; SameSite=None; Secure";


// because who wants to type this every time?
var twitch = window.Twitch.ext;


//run at application launch
twitch.onContext(function(context) {
    twitch.rig.log(context);
});

//request the JWT token from twitch
twitch.onAuthorized(function(auth) {
    // save our credentials
    token = auth.token;
    tuid = auth.userId;
    
       
});

function updatePred(pred) {

    twitch.rig.log('Displaying prediction');
    document.getElementById("prediction").innerHTML = pred;    
}

function logError(_, error, status) {

  twitch.rig.log('EBS request returned '+status+' ('+error+')');
}

function logSuccess(pred, status) {
  // we could also use the output to update the block synchronously here,
  // but we want all views to get the same broadcast response at the same time.
  twitch.rig.log('success');
  twitch.rig.log('EBS request returned '+pred+' ('+status+')');
}

//graph 1 config
// <block:setup:1>
const labels = [
    't-6',
    't-5',
    't-4',
    't-3',
    't-2',
    't-1',
    't0',
    't+1',
    't+2',
    't+3',
];

//initialize graph curve data
var preds = [0.0,0.0,0.0];

var curve_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

var fulldata = curve_data.concat(preds);


var empty1= new Array(curve_data.length - 1);
var empty2= new Array(preds.length);

// </block:data>
const data = {
    labels: labels,
    datasets: [{
    label: 'sentiment',
    data: curve_data.concat(empty2),
    backgroundColor: 'blue',      
    borderColor: 'blue'
    },
    {
    label: 'prediction',
    data: empty1.concat(curve_data[curve_data.length - 1],preds),
    backgroundColor: 'white',      
    borderColor: 'green',
    borderDash: [6,6]
    }
    ]
};

twitch.rig.log(data.datasets);

// </block:setup>

const genericOptions = {
    fill: false,
    interaction: {
      intersect: false
    },
    radius: 0,
    plugins: {
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
    hover: {
        mode: 'index',
        intersec: false
      },
    scales: {
        x: {
          title: {
            display: true,
            text: 'time'
          },
          grid:{
            color : 'rgb(100,100,100)',
            borderDash : [5,5]
          }
        },
        y: {
          title: {
            display: true,
            text: 'sentiment'
          },
          
          ticks: {
            // forces step size to be 0.1 units
            stepSize: 0.1
          },
          grid:{
            color : 'rgb(100,100,100)',
            borderDash : [5,5]
          }
        }
      }
  };


  
// <block:config:0>
const config = {
    type: 'line',
    data: data,
    responsive : true,
    options: genericOptions
};



//main function
$(function() {



    //display graph
    const myChart = new Chart(
      document.getElementById('myChart'),
      config
    );   



    // listen for incoming broadcast message from our EBS
    twitch.listen('broadcast', function (target, contentType, value) {
        twitch.rig.log('Received broadcast prediction');

        //debug recieved data
        twitch.rig.log(target)
        twitch.rig.log(contentType)
        twitch.rig.log(value)

        twitch.rig.log(typeof value)

        //update the panel
        updatePred(value);

        //update graph curve data

        curve_data.shift();

        curve_data.push(parseFloat(JSON.parse(value).sentiment));

        preds = JSON.parse(value).pred

        myChart.data.datasets[0].data = curve_data.concat(empty2);
        myChart.data.datasets[1].data = empty1.concat(curve_data[curve_data.length - 1],preds);

        twitch.rig.log(curve_data.concat(preds))

        //update graph
        myChart.update();


    });

    
     
   

});
