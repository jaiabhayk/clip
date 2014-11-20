jQuery(document).ready(function(){
	
	jQuery('.footer-top-area .col-md-4.col-sm-4:first-child > .single_widget').addClass('first-widget');

  jQuery.get( "https://api-calls.p.mashape.com/total?mashape-key=MmWbaTYfEumshpmM7U8LTeSjIVtwp1Au50ajsny3jtBF9URYa3", function( data ) {
    jQuery( "#apiCalls" ).html( commaSeparateNumber(data.total) );
    var start = data.total;
    setInterval(function(){
      jQuery( "#apiCalls" ).html( commaSeparateNumber(start++) );
    },10);
  });
  

  jQuery.get( "https://mashape.p.mashape.com/apis?mashape-key=d3QWzc2RL60AtFVNx6s7bxOdrnUcl9Lu", function( data ) {
    jQuery( "#totalAPIs" ).html( commaSeparateNumber(data.total) );
  });


  jQuery.getJSON("https://api.twitter.com/1/statuses/user_timeline/mashape.json?count=1&include_rts=1&callback=?", function(data) {
    jQuery("#twitterContent").html(data[0].text);
  });

		
});

function commaSeparateNumber(val){
  while (/(\d+)(\d{3})/.test(val.toString())){
    val = val.toString().replace(/(\d+)(\d{3})/, '$1'+','+'$2');
  }
  return val;
}

window.analytics=window.analytics||[],window.analytics.methods=["identify","group","track","page","pageview","alias","ready","on","once","off","trackLink","trackForm","trackClick","trackSubmit"],window.analytics.factory=function(t){return function(){var a=Array.prototype.slice.call(arguments);return a.unshift(t),window.analytics.push(a),window.analytics}};for(var i=0;i<window.analytics.methods.length;i++){var key=window.analytics.methods[i];window.analytics[key]=window.analytics.factory(key)}window.analytics.load=function(t){if(!document.getElementById("analytics-js")){var a=document.createElement("script");a.type="text/javascript",a.id="analytics-js",a.async=!0,a.src=("https:"===document.location.protocol?"https://":"http://")+"cdn.segment.io/analytics.js/v1/"+t+"/analytics.min.js";var n=document.getElementsByTagName("script")[0];n.parentNode.insertBefore(a,n)}},window.analytics.SNIPPET_VERSION="2.0.9",
window.analytics.load("bh0h42tg71");
window.analytics.page();