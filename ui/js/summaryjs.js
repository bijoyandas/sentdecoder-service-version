summaryEnter = function(event) {
	if (event.keyCode == 13) {
		sendLink();
	}
}


function errorSnackBar(error)
{
	'use strict';
	var snackbarContainer = document.querySelector('#error_snackbar');
	var showToastButton = document.querySelector('#demo-show-toast');
	'use strict';
	  var data = {
		      message: error,
		      timeout: 2000,
		      actionHandler: function(){},
		      actionText: 'OK'
		    };
	snackbarContainer.MaterialSnackbar.showSnackbar(data);
}

function sendLink() {
	var v=document.search.article.value;
	if (v==null || v=="")
		errorSnackBar('Enter an article link to analyze');
	else {
		var progress="<div class='progress' style='width:600px;margin:auto'><div class='indeterminate'></div></div>";
		document.getElementById('summaryData').innerHTML=progress;
		document.search.article.disabled = true;
		document.search.summarize.disabled = true;
		var url="https://sentdecoderservice.cfapps.eu10.hana.ondemand.com/article/summary";

		if(window.XMLHttpRequest){
			request=new XMLHttpRequest();
		}
		else if(window.ActiveXObject){
			request=new ActiveXObject("Microsoft.XMLHTTP");
		}

		try
		{
			request.onreadystatechange=getInfo;
			request.open("POST",url,true);
			request.send(JSON.stringify({ "url": v}));
		}
		catch(e)
		{
			alert("Unable to connect to server");
		}
	}
}

function getInfo() {
	if(request.readyState==4){
		document.search.article.disabled = false;
		document.search.summarize.disabled = false;
		var val=request.responseText;
		var results = JSON.parse(val).results;
		var sentences = results.sentences;
		var sentiment = results.polarity;
		if (sentiment == 0) {
			sentColor = '#e2d922';
			sentText = 'Neutral Article';
		}
		else if (sentiment > 0 && sentiment < 0.50) {
			sentColor = '#bbe222';
			sentText = 'Partially Positive';
		}
		else if (sentiment > 0.50) {
			sentColor = '#22e29b';
			sentText = 'Extremely Positive';
		}
		else if (sentiment <0 && sentiment > -0.50) {
			sentColor = '#e28522';
			sentText = 'Partially Negative';
		}
		else if (sentiment < -0.50) {
			sentColor = '#e23e22';
			sentText = 'Extremely Negative';
		}
		var summarySents = '<div style="padding-top:10px;text-align:left"><div style="width:100%;font-size:20px;padding-left:120px;padding-right:120px;text-align:left">Sentiment: <span style="color:#ffffff;background-color:'+sentColor+';padding:5px;border-radius:3px">'+sentText+'</span></div></div><div style="padding-top:10px;font-size:20px;padding-left:120px;padding-right:120px;text-align:left"><ul><li>'+sentences[0]+'</li><li>'+sentences[1]+'</li><li>'+sentences[2]+'</li><li>'+sentences[3]+'</li><li>'+sentences[4]+'</li></ul></div>';
		document.getElementById('summaryData').innerHTML = summarySents;
	}
}
