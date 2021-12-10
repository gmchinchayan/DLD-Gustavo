var token = "";
var tuid = "";
var ebs = "";

// because who wants to type this every time?
var twitch = window.Twitch.ext;

// create the request options for our Twitch API calls
var requests = {
    set: createRequest('POST', 'increment'),
    get: createRequest('GET', 'current')
};

function createRequest(type, method) {

    r = {
        type: type,
        url: location.protocol + '//localhost:8081/count/' + method,
        success: updateCount,
        error: logError
    };

    //twitch.rig.log('requesting...');
    //twitch.rig.log(r);

    

    return r
}

function setAuth(token) {
    Object.keys(requests).forEach((req) => {
        twitch.rig.log('Setting auth headers');
        requests[req].headers = { 'Authorization': 'Bearer ' + token }
    });
}

twitch.onContext(function(context) {
    twitch.rig.log(context);
});

twitch.onAuthorized(function(auth) {
    // save our credentials
    token = auth.token;
    tuid = auth.userId;

    // enable the button
    $('#increment').removeAttr('disabled');

    setAuth(token);

    twitch.rig.log(JSON.stringify(requests));

    $.ajax(requests.get);
});

function updateCount(nb) {

    //twitch.rig.log(JSON.stringify(nb));

    twitch.rig.log('Updating Count');
    document.getElementById("value").innerHTML = nb.message;

    
}

function logError(_, error, status) {
  twitch.rig.log('EBS request returned '+status+' ('+error+')');
}

function logSuccess(nb, status) {
  // we could also use the output to update the block synchronously here,
  // but we want all views to get the same broadcast response at the same time.
  twitch.rig.log('success');
  twitch.rig.log('EBS request returned '+nb+' ('+status+')');
}

$(function() {

    // when we click the cycle button
    $('#increment').click(function() {
        if(!token) { return twitch.rig.log('Not authorized'); }
        twitch.rig.log('Requesting a count increase');
        
        $.ajax(requests.set);
    });

    // listen for incoming broadcast message from our EBS
    twitch.listen('broadcast', function (target, contentType, value) {
    twitch.rig.log('Received broadcast count');

    updateCount(value);
    });
});
