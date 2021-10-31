var token = "";
var tuid = "";
var ebs = "";

var APIgetway ="https://gaefmvqicb.execute-api.eu-central-1.amazonaws.com/default/";

// because who wants to type this every time?
var twitch = window.Twitch.ext;

// create the request options for our Twitch API calls
var requests = {
    set: createRequest('POST', 'echo')   
};

function createRequest(type, method) {

    r = {
        type: type,
        url: APIgetway + method,
        success: updatePred,
        error: logError
    };

    //twitch.rig.log('requesting...');
    //twitch.rig.log(r);

    

    return r
}

function setAuth(token) {
    Object.keys(requests).forEach((req) => {
        twitch.rig.log('Setting auth headers');
        requests[req].headers = {'Authorization': 'Bearer ' + token }
    });
}


twitch.onContext(function(context) {
    twitch.rig.log(context);
});

twitch.onAuthorized(function(auth) {
    // save our credentials
    token = auth.token;
    tuid = auth.userId;

    
    setAuth(token);

    //twitch.rig.log(JSON.stringify(requests));

    //$.ajax(requests.get);
});

function updatePred(pred) {

    //twitch.rig.log(JSON.stringify(nb));

    twitch.rig.log('Displaying prediction');
    document.getElementById("prediction").innerHTML = pred.message;

    
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

$(function() {

    // when we click the cycle button
    $('#send').click(function() {
        if(!token) { return twitch.rig.log('Not authorized'); }
        twitch.rig.log('Requesting comment sentiment prediction');

        var comment = "";
        comment=document.getElementById("sendComment").value;

        twitch.rig.log('here1');

        mybody = {"message": comment};

        
        
        requests.set.data = mybody;
        requests.set.contentType="text/plain";
        //twitch.rig.log("the request:"+ JSON.stringify(requests.set));
        twitch.rig.log('here2');
        twitch.rig.log("the request:"+ JSON.stringify({method: "POST",url: APIgetway +"echo",headers: requests.set.headers,data: mybody}));        
        twitch.rig.log('here3');


        req={method: "POST",url: APIgetway +"echo",headers: requests.set.headers,data: mybody,crossDomain: true,success: updatePred,error: logError};
        twitch.rig.log('here4');
        $.ajax(req);

        twitch.rig.log('here5');
    


    });

    // listen for incoming broadcast message from our EBS
    twitch.listen('broadcast', function (target, contentType, value) {
    twitch.rig.log('Received broadcast prediction');
    twitch.rig.log(target)
    twitch.rig.log(contentType)
    twitch.rig.log(value)

    updatePred(value);
    });
});
